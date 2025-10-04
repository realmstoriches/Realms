import logging
import json
import os
from agentic_launchpad.modules.upsell_agent import generate_upsell_payload
from agentic_launchpad.modules.email_campaign.thank_you_agent import send_thank_you_email

logging.basicConfig(level=logging.INFO)

def escalate_if_needed(role, crew, manifest):
    fallback_agent = next(
        (r for r in manifest.get("expanded_roles", [])
         if r.get("role_title") == role and r.get("crew") != crew.get("crew_name")),
        None
    )

    if fallback_agent:
        fallback_crew = fallback_agent.get("crew", "Unknown")
        agent_name = fallback_agent.get("agent_name", "Unknown")
        logging.info(f"🔁 Escalated role {role} to fallback crew {fallback_crew} → {agent_name}")
        log_escalation(role, crew.get("crew_name", "Unknown"), fallback_crew, agent_name)

        # Trigger upsell and thank-you flows
        upsell = generate_upsell_payload(agent_name, fallback_crew)
        send_thank_you_email(agent_name, fallback_crew, upsell)
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