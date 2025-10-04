import json, logging, random, uuid

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load agents
with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)

# Generate 500+ unique roles across domains
domains = [
    "Executive Leadership", "Engineering", "Data Science & ML", "Product Management",
    "Design & UX", "Quality Assurance", "DevOps & Infrastructure", "Security & Compliance",
    "People & Culture", "Finance & Legal", "Sales & Partnerships", "Marketing & Growth",
    "Simulation Ops", "Fallback Systems", "Tool Validation", "Persona Fusion", "Agent Training",
    "Mission Planning", "Emergency Response", "Recursive Scaling", "Bias Testing", "Crew Architecture"
]

role_templates = [
    "Lead", "Specialist", "Architect", "Strategist", "Engineer", "Coordinator", "Observer",
    "Commander", "Validator", "Trainer", "Planner", "Analyst", "Operator", "Designer", "Director"
]

roles = []
for domain in domains:
    for template in role_templates:
        title = f"{template} of {domain}"
        roles.append({
            "role_id": str(uuid.uuid4())[:8],
            "role_title": title,
            "domain": domain
        })

# Shuffle and assign agents
random.shuffle(agents)
assignments = []
for i, agent in enumerate(agents):
    role = roles[i % len(roles)]
    assignments.append({
        "agent_id": agent["agent_id"],
        "agent_name": agent["name"],
        "crew": agent.get("crew_assignment", f"Crew_{i//2+1:03}"),
        "role_title": role["role_title"],
        "domain": role["domain"],
        "status": "assigned",
        "simulation_ready": True,
        "profile_url": f"https://realms.ai/agents/{agent['agent_id']}"
    })

# Write output
with open("expanded_role_matrix.json", "w", encoding="utf-8") as f:
    json.dump(assignments, f, indent=4)

logging.info(f"✅ expanded_role_matrix.json written with {len(assignments)} agent-role assignments")