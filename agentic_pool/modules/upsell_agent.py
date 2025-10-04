from datetime import datetime

def generate_upsell_payload(agent_name, crew_name):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    title = f"🛒 Upsell Opportunity: {agent_name}"
    message = (
        f"{agent_name} from crew {crew_name} was activated as a fallback agent.\n"
        f"This is a prime moment to offer premium tools, priority access, or exclusive upgrades."
    )
    cta = "Upgrade Now → https://realms.ai/upgrade"

    payload = {
        "title": title,
        "message": message,
        "cta": cta,
        "timestamp": timestamp,
        "crew": crew_name,
        "agent": agent_name
    }

    print(f"📈 Upsell payload generated for {agent_name} in {crew_name} @ {timestamp}")
    return payload

