"""
This module defines the logic for creating and managing different
agent arrangements for various operational domains.
"""
import json
import os
from src.company import ORG_CHART, generate_employee_file
from src.agent import Agent
from src.knowledge import KnowledgeBase

ARRANGEMENT_TEMPLATES = {
    "Development": {
        "optimization_focus": "Engineering and R&D",
        "roles": [
            "AI Infrastructure Engineer",
            "Graphics Driver Engineer",
            "ASIC Design Engineer",
            "Research Scientist"
        ]
    },
    "Launch": {
        "optimization_focus": "Product Launch and Marketing",
        "roles": [
            "Graphics Driver Engineer",
            "AI Infrastructure Engineer",
            # In a real scenario, we would add marketing and sales roles.
            # For now, we reuse existing roles to demonstrate the concept.
        ]
    }
}

def generate_manifest(arrangement_name: str, template: dict, output_dir="arrangements"):
    """
    Generates a manifest.json file for a given arrangement.

    The manifest includes the agent roster, optimization focus, and other metadata.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Find all role definitions from the main ORG_CHART
    all_roles = {role['title']: role for dept_roles in ORG_CHART.values() for role in dept_roles}

    agent_roster = []
    for role_title in template["roles"]:
        if role_title in all_roles:
            role_def = all_roles[role_title]
            employee_file = generate_employee_file(role_def)
            agent_roster.append(employee_file)

    manifest = {
        "arrangement_name": arrangement_name,
        "optimization_focus": template["optimization_focus"],
        "agent_roster": agent_roster,
        "chroma_db_linkage": "shared_workforce_kb", # Placeholder
        "arbitration_logic_parameters": {"fallback_heuristic": "A", "weights": {"A": 1.0, "B": 1.0}} # Placeholder
    }

    manifest_path = os.path.join(output_dir, f"{arrangement_name.lower()}_manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)

    print(f"Generated manifest for '{arrangement_name}' at {manifest_path}")
    return manifest_path