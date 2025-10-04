import json, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load agent roster and crew manifest
with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)
with open("crew_manifest.json", "r", encoding="utf-8") as f:
    crews = json.load(f)

# Index agents by domain
domain_map = {}
for agent in agents:
    domain = agent.get("domain", "General")
    if domain not in domain_map:
        domain_map[domain] = []
    domain_map[domain].append(agent)

# Start Mermaid diagram
lines = ["```mermaid", "graph TD", 'Company["🧠 Realms AI Systems"]']

# Define departments
departments = {
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

# Build department nodes
for dept, roles in departments.items():
    dept_id = dept.replace(" ", "_").replace("&", "And")
    lines.append(f'Company --> {dept_id}["{dept}"]')
    for role in roles:
        # Assign a random agent from matching domain
        candidates = domain_map.get(dept.split()[0], []) or domain_map.get("General", [])
        agent = candidates.pop(0) if candidates else {"name": "Unassigned", "agent_id": "null"}
        role_id = role.replace(" ", "_")
        lines.append(f'{dept_id} --> {role_id}["{role}: {agent["name"]}"]')
        lines.append(f'click {role_id} "https://realms.ai/agents/{agent["agent_id"]}" "View {agent["name"]} profile"')

# Add simulation flow
lines += [
    "",
    "%% Simulation Flow",
    "flowchart LR",
    'Start["🧠 Simulation Trigger"] --> CrewAlpha001["Crew_Alpha_001"]',
    "CrewAlpha001 --> PM",
    "CrewAlpha001 --> Eng",
    "CrewAlpha001 --> DS",
    "CrewAlpha001 --> DevOps",
    "PM --> UX",
    "Eng --> QA",
    "DS --> Sec",
    "DevOps --> Infra[\"Cloud Infrastructure\"]",
    "QA --> Feedback[\"Simulation Feedback Loop\"]",
    "Feedback --> Start",
    "CrewAlpha001 --> Fallback[\"Fallback Crew Activated\"]",
    "Fallback --> PM"
]

# Close diagram
lines.append("```")

# Write output
with open("mermaid_schematic.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

logging.info("✅ mermaid_schematic.md written with full org chart, agent links, and simulation flow")