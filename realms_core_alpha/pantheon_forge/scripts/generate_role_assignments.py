import json, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load agent roster and crew manifest
with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)
with open("crew_manifest.json", "r", encoding="utf-8") as f:
    crews = json.load(f)

# Index agents by name
agent_index = {a["name"]: a for a in agents}

# Define department-role schema
org_roles = {
    "Executive Leadership": ["CEO", "CTO", "COO"],
    "Engineering": ["Frontend Engineer", "Backend Engineer", "API Architect", "AI Integration Engineer"],
    "Data Science & ML": ["ML Engineer", "Data Scientist", "NLP Specialist", "Computer Vision Lead"],
    "Product Management": ["Head of Product", "Technical PM", "Strategic PM"],
    "Design & UX": ["UX Director", "UI Designer", "User Researcher"],
    "Quality Assurance": ["QA Lead", "Automation Tester", "Manual Tester"],
    "DevOps & Infrastructure": ["DevOps Lead", "Cloud Engineer", "CI/CD Specialist"],
    "Security & Compliance": ["CISO", "Security Engineer", "Risk Analyst"],
    "People & Culture": ["HR Director", "Recruiter", "Culture Ops"],
    "Finance & Legal": ["CFO", "Legal Counsel", "Compliance Officer"],
    "Sales & Partnerships": ["CRO", "Account Exec", "Business Dev Manager"],
    "Marketing & Growth": ["CMO", "Growth Hacker", "Content Strategist"]
}

# Assign agents to roles
assignments = []
used_agents = set()

for dept, roles in org_roles.items():
    for role in roles:
        # Find first unused agent from matching domain
        candidates = [a for a in agents if a["domain"] in dept and a["name"] not in used_agents]
        agent = candidates[0] if candidates else {"name": "Unassigned", "agent_id": "null", "crew_assignment": "Unassigned", "status": "unassigned"}
        used_agents.add(agent["name"])
        assignments.append({
            "department": dept,
            "role": role,
            "agent_id": agent["agent_id"],
            "agent_name": agent["name"],
            "crew": agent.get("crew_assignment", "Unassigned"),
            "status": agent.get("status", "unassigned"),
            "profile_url": f"https://realms.ai/agents/{agent['agent_id']}"
        })

# Write output
with open("role_assignments.json", "w", encoding="utf-8") as f:
    json.dump(assignments, f, indent=4)

logging.info(f"✅ role_assignments.json written with {len(assignments)} role mappings")