import json
import os
from collections import defaultdict

def build_manifest():
    SOURCE_DIR = os.path.dirname(__file__)
    OUTPUT_PATH = os.path.join(SOURCE_DIR, "company_manifest.json")

    manifest = {"crews": [], "expanded_roles": []}
    crews = set()
    roles_seen = set()

    def load_json(filename):
        path = os.path.join(SOURCE_DIR, filename)
        if not os.path.exists(path):
            print(f"⚠️ Missing file: {filename}")
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    agent_entries = load_json("agents.json")
    crew_entries = load_json("crews.json")
    fallback_entries = load_json("fallbacks.json")

    for crew in crew_entries:
        crew_name = crew.get("crew_name")
        if crew_name and crew_name not in crews:
            manifest["crews"].append({"crew_name": crew_name})
            crews.add(crew_name)

    for entry in agent_entries:
        name = entry.get("name")
        role = entry.get("role_title")
        crew = entry.get("crew")

        if not name or not role or not crew:
            print(f"⚠️ Skipping malformed agent entry: {entry}")
            continue

        key = (name, role, crew)
        if key not in roles_seen:
            manifest["expanded_roles"].append({
                "agent_name": name,
                "role_title": role,
                "crew": crew
            })
            roles_seen.add(key)
            if crew not in crews:
                manifest["crews"].append({"crew_name": crew})
                crews.add(crew)

    for fallback in fallback_entries:
        role = fallback.get("role_title")
        fallback_names = fallback.get("fallbacks", [])
        for name in fallback_names:
            crew = f"FallbackCrew_{role.replace(' ', '')}"
            key = (name, role, crew)
            if key not in roles_seen:
                manifest["expanded_roles"].append({
                    "agent_name": name,
                    "role_title": role,
                    "crew": crew
                })
                roles_seen.add(key)
                if crew not in crews:
                    manifest["crews"].append({"crew_name": crew})
                    crews.add(crew)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    print(f"\n✅ company_manifest.json built with {len(manifest['expanded_roles'])} agents across {len(manifest['crews'])} crews")

if __name__ == "__main__":
    build_manifest()