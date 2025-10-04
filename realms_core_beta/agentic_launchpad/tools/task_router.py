import json, logging
from fallback_manager import escalate_if_needed
from agent_output_generator import generate_output
from tool_executor import execute_tool

logging.basicConfig(level=logging.INFO)

def route_task(mission, crew, manifest):
    required_roles = mission["required_roles"]
    assigned_agents = []

    for role in required_roles:
        match = next(
            (r for r in manifest["expanded_roles"]
             if r["role_title"] == role and r["crew"] == crew["crew_name"]),
            None
        )
        if match:
            assigned_agents.append(match["agent_name"])
        else:
            logging.warning(f"⚠️ Role {role} not found in crew {crew['crew_name']}")
            escalate_if_needed(role, crew, manifest)

    for agent in assigned_agents:
        role = next(
            (r["role_title"] for r in manifest["expanded_roles"]
             if r["agent_name"] == agent and r["crew"] == crew["crew_name"]),
            "Unknown"
        )
        output_file = generate_output(agent, role, mission, crew.get("tool_access", []))
        execute_tool(output_file)

    update_status(crew["crew_name"], assigned_agents, mission["mission_id"])

def update_status(crew_id, agents, mission_id):
    status = {
        "crew": crew_id,
        "agents": agents,
        "mission_id": mission_id,
        "status": "active"
    }
    with open("crew_status.json", "w") as f:
        json.dump(status, f, indent=4)
    with open("launch_log.txt", "a", encoding="utf-8") as log:
        log.write(f"{mission_id} -> {crew_id} -> {agents}\n")
    logging.info(f"✅ Mission {mission_id} routed to {crew_id}")