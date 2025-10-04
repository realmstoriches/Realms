import json
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Simulate a crew meeting
def simulate_meeting(agent):
    name = agent["name"]
    alpha = agent["persona"]["alpha_overlay"]
    beta = agent["persona"]["beta_overlay"]
    unified = agent["persona"]["unified_overlay"]

    decision = random.choice([
        "Approve new tool integration",
        "Flag knowledge gap in source ingestion",
        "Request override from founder",
        "Deploy simulation protocol",
        "Initiate recursive agent spawn"
    ])

    logging.info(f"🧠 {name} meeting:")
    logging.info(f"Alpha: {alpha}")
    logging.info(f"Beta: {beta}")
    logging.info(f"Unified: {unified}")
    logging.info(f"🗳 Decision: {decision}")
    return {
        "agent": name,
        "decision": decision
    }

# ✅ Main runner
if __name__ == "__main__":
    with open("agent_manifest.json", "r", encoding="utf-8") as f:
        agents = json.load(f)

    decisions = []
    for agent in agents[:50]:  # Simulate first 50 agents
        result = simulate_meeting(agent)