import json
import os
from collections import defaultdict

SOURCE_DIR = os.path.dirname(__file__)
AGENTS_PATH = os.path.join(SOURCE_DIR, "agents.json")
FALLBACKS_PATH = os.path.join(SOURCE_DIR, "fallbacks.json")
REPORT_PATH = os.path.join(SOURCE_DIR, "fallback_audit_report_v2.json")

def load_json(path):
    if not os.path.exists(path):
        print(f"Missing file: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def audit_all_roles():
    agents = load_json(AGENTS_PATH)
    fallbacks = load_json(FALLBACKS_PATH)

    role_to_agents = defaultdict(list)
    fallback_roles = set(entry["role_title"] for entry in fallbacks)

    for agent in agents:
        role = agent.get("role_title")
        name = agent.get("name")
        if role and name:
            role_to_agents[role].append(name)

    roles_with_single_agent = []
    roles_missing_fallback_entry = []
    roles_fully_covered = []

    for role, names in role_to_agents.items():
        if len(names) == 1:
            roles_with_single_agent.append({"role": role, "agent": names[0]})
        elif role not in fallback_roles:
            roles_missing_fallback_entry.append({"role": role, "agents": names})
        else:
            roles_fully_covered.append({"role": role, "agents": names})

    report = {
        "summary": {
            "total_roles": len(role_to_agents),
            "roles_with_single_agent": len(roles_with_single_agent),
            "roles_missing_fallback_entry": len(roles_missing_fallback_entry),
            "roles_fully_covered": len(roles_fully_covered)
        },
        "roles_with_single_agent": roles_with_single_agent,
        "roles_missing_fallback_entry": roles_missing_fallback_entry,
        "roles_fully_covered": roles_fully_covered
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)

    print("✅ Full fallback audit complete. Report saved to fallback_audit_report_v2.json")

if __name__ == "__main__":
    audit_all_roles()