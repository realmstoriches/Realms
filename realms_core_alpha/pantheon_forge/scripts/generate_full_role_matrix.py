import json, logging, random

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load agents and crews
with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)
with open("dual_brain_manifest.json", "r", encoding="utf-8") as f:
    crews = json.load(f)

# Define exhaustive role list
roles = {
    "Executive Leadership": ["CEO", "CTO", "COO", "Chief Strategy Officer"],
    "Engineering": ["Frontend Engineer", "Backend Engineer", "API Architect", "AI Integration Engineer", "Platform Engineer", "Systems Architect"],
    "Data Science & ML": ["ML Engineer", "Data Scientist", "NLP Specialist", "Computer Vision Lead", "Model Ops Engineer"],
    "Product Management": ["Head of Product", "Technical PM", "Strategic PM", "Growth PM"],
    "Design & UX": ["UX Director", "UI Designer", "User Researcher", "Interaction Designer"],
    "Quality Assurance": ["QA Lead", "Automation Tester", "Manual Tester", "Test Architect"],
    "DevOps & Infrastructure": ["DevOps Lead", "Cloud Engineer", "CI/CD Specialist", "Infra Reliability Engineer"],
    "Security & Compliance": ["CISO", "Security Engineer", "Risk Analyst", "Compliance Architect"],
    "People & Culture": ["HR Director", "Recruiter", "Culture Ops", "Org Designer"],
    "Finance & Legal": ["CFO", "Legal Counsel", "Compliance Officer", "Financial Analyst"],
    "Sales & Partnerships": ["CRO", "Account Exec", "Business Dev Manager", "Partner Strategist"],
    "Marketing & Growth": ["CMO", "Growth Hacker", "Content Strategist", "Brand Architect"]
}

# Flatten roles
all_roles = []
for dept, titles in roles.items():
    for title in titles:
        all_roles.append({"department": dept, "role": title})

# Shuffle crews and assign roles
random.shuffle(crews)
assignment_matrix = []
used_agents = set()

for i, role in enumerate(all_roles):
    crew = crews[i % len(crews)]
    alpha = crew["alpha"]
    beta = crew["beta"]
    assignment_matrix.append({
        "department": role["department"],
        "role": role["role"],
        "crew": crew["crew"],
        "alpha": alpha,
        "beta": beta,
        "status": "assigned",
        "simulation_ready": True
    })
    used_agents.update([alpha, beta])

# Write output
with open("full_role_matrix.json", "w", encoding="utf-8") as f:
    json.dump(assignment_matrix, f, indent=4)

logging.info(f"✅ full_role_matrix.json written with {len(assignment_matrix)} complete role assignments")