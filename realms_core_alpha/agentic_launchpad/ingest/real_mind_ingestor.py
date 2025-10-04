import json
import os
import logging
from collections import defaultdict
from random import choice

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SOURCE_DIR = os.path.dirname(__file__)
REAL_MINDS_PATH = os.path.join(SOURCE_DIR, "real_minds.json")
AGENTS_PATH = os.path.join(SOURCE_DIR, "agents.json")
CREWS_PATH = os.path.join(SOURCE_DIR, "crews.json")
TEAMS_PATH = os.path.join(SOURCE_DIR, "teams.json")
DEPARTMENTS_PATH = os.path.join(SOURCE_DIR, "departments.json")
FALLBACKS_PATH = os.path.join(SOURCE_DIR, "fallbacks.json")
MANIFEST_BUILDER_PATH = os.path.join(SOURCE_DIR, "ingest_modular_manifest.py")

def load_real_minds():
    if not os.path.exists(REAL_MINDS_PATH):
        logging.error("❌ real_minds.json not found")
        return []

    with open(REAL_MINDS_PATH, "r", encoding="utf-8") as f:
        raw = "[" + f.read().strip().rstrip(",") + "]"

    def flatten(data):
        flat = []
        def recurse(entry):
            if isinstance(entry, list):
                for item in entry:
                    recurse(item)
            elif isinstance(entry, dict):
                flat.append(entry)
        recurse(json.loads(raw))
        return flat

    return flatten(json.loads(raw))

def assign_role(name):
    roles = [
        "Strategic PM", "UI Designer", "Frontend Engineer", "Systems Architect",
        "Product Lead", "QA Analyst", "Ops Coordinator"
    ]
    return choice(roles)

def assign_team(role):
    return {
        "Strategic PM": "Leadership",
        "UI Designer": "Design",
        "Frontend Engineer": "Engineering",
        "Systems Architect": "Engineering",
        "Product Lead": "Product",
        "QA Analyst": "Quality",
        "Ops Coordinator": "Operations"
    }.get(role, "General")

def assign_department(team):
    return {
        "Leadership": "Strategy",
        "Design": "Product",
        "Engineering": "Technology",
        "Operations": "Execution",
        "Product": "Product",
        "Quality": "Technology",
        "General": "Misc"
    }.get(team, "Misc")

def build_all():
    minds = load_real_minds()
    if not minds:
        return

    valid_minds = []
    seen = set()
    for mind in minds:
        if not all(k in mind for k in ["name", "domain", "contribution"]):
            continue
        name = mind["name"].strip()
        if name.lower() not in seen:
            seen.add(name.lower())
            valid_minds.append(name)

    logging.info(f"✅ {len(valid_minds)} unique valid minds")

    agents = []
    crews = defaultdict(list)
    teams = defaultdict(list)
    departments = defaultdict(set)
    fallbacks = defaultdict(list)

    for name in valid_minds:
        role = assign_role(name)
        team = assign_team(role)
        department = assign_department(team)
        crew = f"Crew_{team}_{role.replace(' ', '')}"

        agents.append({
            "name": name,
            "role_title": role,
            "crew": crew,
            "team": team,
            "department": department,
            "fallback_for": []
        })

        crews[crew].append(name)
        teams[team].append(name)
        departments[department].add(team)
        fallbacks[role].append(name)

    with open(AGENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(agents, f, indent=4)

    with open(CREWS_PATH, "w", encoding="utf-8") as f:
        json.dump([{"crew_name": k, "mission_scope": f"{k} mission", "agents": v} for k, v in crews.items()], f, indent=4)

    with open(TEAMS_PATH, "w", encoding="utf-8") as f:
        json.dump([{"team_name": k, "function": f"{k} function", "members": v} for k, v in teams.items()], f, indent=4)

    with open(DEPARTMENTS_PATH, "w", encoding="utf-8") as f:
        json.dump([{"department_name": k, "teams": sorted(list(v))} for k, v in departments.items()], f, indent=4)

    fallback_out = []
    for role, names in fallbacks.items():
        if len(names) > 1:
            fallback_out.append({
                "role_title": role,
                "primary": names[0],
                "fallbacks": names[1:]
            })
    with open(FALLBACKS_PATH, "w", encoding="utf-8") as f:
        json.dump(fallback_out, f, indent=4)

    logging.info("✅ Modular files generated")

    if os.path.exists(MANIFEST_BUILDER_PATH):
        try:
            with open(MANIFEST_BUILDER_PATH, "r", encoding="utf-8") as f:
                code = f.read()
                exec(code)
        except Exception as e:
            logging.error(f"❌ Failed to build company_manifest.json: {e}")
    else:
        logging.error("❌ ingest_modular_manifest.py not found")

if __name__ == "__main__":
    build_all()