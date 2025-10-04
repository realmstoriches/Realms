import json
from collections import defaultdict

MANIFEST_PATH = "agentic_launchpad/company_manifest.json"

def analyze_manifest():
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    roles_by_crew = defaultdict(list)
    agents_by_role = defaultdict(list)
    crews = set()
    agents = set()

    for entry in manifest.get("expanded_roles", []):
        name = entry.get("agent_name")
        role = entry.get("role_title")
        crew = entry.get("crew")

        if not name or not role or not crew:
            continue

        crews.add(crew)
        agents.add(name)
        roles_by_crew[crew].append(role)
        agents_by_role[role].append(name)

    print(f"\n🧠 Manifest Summary")
    print(f"• Total agents: {len(agents)}")
    print(f"• Total crews: {len(crews)}")
    print(f"• Unique roles: {len(agents_by_role)}\n")

    print("📦 Roles by Crew:")
    for crew, roles in roles_by_crew.items():
        print(f"  - {crew}: {sorted(set(roles))}")

    print("\n👥 Agents by Role:")
    for role, names in agents_by_role.items():
        print(f"  - {role}: {sorted(set(names))}")

    missing_roles = [r for r, names in agents_by_role.items() if len(names) < 2]
    if missing_roles:
        print("\n⚠️ Roles with weak fallback coverage (only one agent):")
        for role in missing_roles:
            print(f"  - {role}")

if __name__ == "__main__":
    analyze_manifest()