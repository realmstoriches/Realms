import json
import os
from collections import defaultdict

SOURCE_DIR = os.path.dirname(__file__)
AGENTS_PATH = os.path.join(SOURCE_DIR, "agents.json")
CREWS_PATH = os.path.join(SOURCE_DIR, "crews.json")
FALLBACKS_PATH = os.path.join(SOURCE_DIR, "fallbacks.json")
OUTPUT_PATH = os.path.join(SOURCE_DIR, "crew_role_matrix.json")

def load_json(path):
    if not os.path.exists(path):
        print(f"Missing file: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_matrix():
    agents = load_json(AGENTS_PATH)
    crews = load_json(CREWS_PATH)
    fallbacks = load_json(FALLBACKS_PATH)

    crew_roles = defaultdict(lambda: defaultdict(list))
    role_fallbacks = defaultdict(list)

    for agent in agents:
        crew = agent.get("crew")
        role = agent.get("role_title")
        name = agent.get("name")
        if crew and role and name:
            crew_roles[crew][role].append(name)

    for entry in fallbacks:
        role = entry.get("role_title")
        backups = entry.get("fallbacks", [])
        for name in backups:
            role_fallbacks[role].append(name)

    matrix = []
    for crew in crews:
        crew_name = crew.get("crew_name")
        roles = crew_roles.get(crew_name, {})
        crew_entry = {"crew_name": crew_name, "roles": []}
        for role, agents in roles.items():
            crew_entry["roles"].append({
                "role_title": role,
                "agents": agents,
                "fallbacks": role_fallbacks.get(role, [])
            })
        matrix.append(crew_entry)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(matrix, f, indent=4)

    print("✅ Crew-role matrix generated: crew_role_matrix.json")

if __name__ == "__main__":
    generate_matrix()