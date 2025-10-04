import json
from pathlib import Path

def define_roles():
    base = Path(__file__).parent.parent
    with open(base / "business" / "company_structure.json") as f:
        roles = json.load(f)
    for role in roles:
        print(f"Defined role: {role['role_name']}")

if __name__ == "__main__":
    define_roles()