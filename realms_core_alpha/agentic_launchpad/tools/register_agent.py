import json
import sys
import os

def register_agent(agent_name, role_title, crew_name, manifest_path="agentic_launchpad/company_manifest.json"):
    if not os.path.exists(manifest_path):
        print(f"❌ Manifest file not found at {manifest_path}")
        return

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    # Ensure crew exists
    if crew_name not in [c["crew_name"] for c in manifest.get("crews", [])]:
        manifest.setdefault("crews", []).append({"crew_name": crew_name})

    # Prevent duplicate agent-role-crew entries
    if any(
        r["agent_name"] == agent_name and
        r["role_title"] == role_title and
        r["crew"] == crew_name
        for r in manifest.get("expanded_roles", [])
    ):
        print(f"⚠️ Agent {agent_name} already registered as {role_title} in {crew_name}")
        return

    # Add agent
    manifest.setdefault("expanded_roles", []).append({
        "agent_name": agent_name,
        "role_title": role_title,
        "crew": crew_name
    })

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"✅ Registered {agent_name} as {role_title} in {crew_name}")

# CLI wrapper
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python register_agent.py 'Agent Name' 'Role Title' 'Crew Name'")
    else:
        register_agent(sys.argv[1], sys.argv[2], sys.argv[3])