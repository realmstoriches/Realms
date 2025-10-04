import json
import os
from datetime import datetime

SOURCE_DIR = "agentic_launchpad"
OUTPUT_PATH = os.path.join(SOURCE_DIR, "company_manifest.json")

def load_json(filename):
    path = os.path.join(SOURCE_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def build_manifest():
    manifest = {"crews": [], "expanded_roles": []}
    crews = {}
    agents = {}

    # Load source files
    roster = load_json("agent_roster.json")
    crew_map = load_json("crew_manifest.json")
    roles = load_json("role_assignments.json")
    real_minds = {m["name"] for m in load_json("real_minds.json")}
    dual_brains = load_json("dual_brain_manifest.json")

    # Build crews from crew_manifest
    for entry in crew_map:
        crew_name = entry.get("crew_name")
        if crew_name and crew_name not in crews:
            crews[crew_name] = []
            manifest["crews"].append({"crew_name": crew_name})

        for agent in entry.get("agents", []):
            agents[agent] = crew_name

    # Build expanded_roles from agent_roster and role_assignments
    combined_entries = roster + roles
    for entry in combined_entries:
        name = entry.get("agent_name") or entry.get("name") or entry.get("full_name")
        role = entry.get("role_title") or entry.get("role") or entry.get("position")

        if not name or not role:
            print(f"⚠️ Skipping entry with missing name or role: {entry}")
            continue

        verified = name in real_minds
        if not verified:
            print(f"⚠️ Unverified agent: {name} — not found in real_minds.json")

        crew = agents.get(name, f"Crew_{role.replace(' ', '')}")
        key = (name, role, crew)

        if key not in {(r["agent_name"], r["role_title"], r["crew"]) for r in manifest["expanded_roles"]}:
            manifest["expanded_roles"].append({
                "agent_name": name,
                "role_title": role,
                "crew": crew
            })
            if crew not in crews:
                manifest["crews"].append({"crew_name": crew})
                crews[crew] = []

    # Add dual-brain fallback logic
    for pair in dual_brains:
        for agent in pair.get("agents", []):
            name = agent.get("name")
            role = agent.get("role")
            crew = agent.get("crew")

            if not name or not role or not crew:
                continue

            if name not in real_minds:
                print(f"⚠️ Skipping fallback agent not in real_minds: {name}")
                continue

            key = (name, role, crew)
            if key not in {(r["agent_name"], r["role_title"], r["crew"]) for r in manifest["expanded_roles"]}:
                manifest["expanded_roles"].append({
                    "agent_name": name,
                    "role_title": role,
                    "crew": crew
                })
                if crew not in crews:
                    manifest["crews"].append({"crew_name": crew})
                    crews[crew] = []

    # Save manifest
    with open(OUTPUT_PATH, "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"✅ company_manifest.json built with {len(manifest['expanded_roles'])} agents across {len(manifest['crews'])} crews")

if __name__ == "__main__":
    build_manifest()