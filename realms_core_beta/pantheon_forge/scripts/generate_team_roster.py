import json, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)

teams = {}
for agent in agents:
    crew = agent.get("crew_assignment", "Unassigned")
    if crew not in teams:
        teams[crew] = []
    teams[crew].append({
        "agent_id": agent["agent_id"],
        "name": agent["name"],
        "role": agent["role_title"],
        "status": agent["status"]
    })

with open("team_roster.json", "w", encoding="utf-8") as f:
    json.dump(teams, f, indent=4)

logging.info(f"✅ team_roster.json written with {len(teams)} teams")