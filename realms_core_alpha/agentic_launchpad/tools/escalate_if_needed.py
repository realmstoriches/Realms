import logging
import json
import os

logging.basicConfig(level=logging.INFO)

def escalate_if_needed(role, crew, manifest):
    fallback_agent = next(
        (r for r in manifest.get("expanded_roles", [])
         if r.get("role_title") == role and r.get("crew") != crew.get("crew_name")),
        None
    )

    if fallback_agent:
        logging.info(f"🔁 Escalated role {role} to fallback crew {fallback_agent['crew']} → {fallback_agent['agent_name']}")
        log_escalation(role, crew["crew_name"], fallback_agent["crew"], fallback_agent["agent_name"])
    else:
        logging.warning(f"❌ No fallback agent found for role {role} in any crew")

def log_escalation(role, original_crew, fallback_crew, agent_name):
    log_entry = {
        "role": role,
        "original_crew": original_crew,
        "fallback_crew": fallback_crew,
        "agent": agent_name
    }
    os.makedirs("logs", exist_ok=True)
    with open("logs/escalation_log.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")