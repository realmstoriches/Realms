def assemble_crew_for_mission(mission, manifest):
    required_roles = mission["required_roles"]
    crew_id = f"DynamicCrew_{mission['mission_id']}"
    assembled_agents = []

    for role in required_roles:
        match = next((r for r in manifest["expanded_roles"] if r["role_title"] == role), None)
        if match:
            assembled_agents.append({
                "agent_name": match["agent_name"],
                "role_title": role,
                "crew": crew_id
            })

    return {
        "crew_name": crew_id,
        "agents": assembled_agents,
        "tool_access": mission.get("tools", [])
    }