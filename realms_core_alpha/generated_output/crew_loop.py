import json

def trigger_followup(mission_id, crew_name, objective, roles, tools):
    new_mission = {
        "mission_id": f"{mission_id}_followup",
        "objective": objective,
        "assigned_crew": crew_name,
        "required_roles": roles,
        "tools": tools,
        "deadline": "2025-10-15"
    }
    with open("agentic_launchpad/mission_queue.json", "r+") as f:
        missions = json.load(f)
        missions.append(new_mission)
        f.seek(0)
        json.dump(missions, f, indent=4)
        f.truncate()
    print(f"🔁 Follow-up mission queued: {new_mission['mission_id']}")