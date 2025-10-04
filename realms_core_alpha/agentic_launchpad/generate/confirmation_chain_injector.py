import json
import os

ROOT_DIR = os.path.abspath("F:/realms_core/agentic_launchpad")
PACKET_DIR = os.path.join(ROOT_DIR, "output", "real_packets")
AGENTS_PATH = os.path.join(ROOT_DIR, "data", "agents.json")

CRITICAL_ROLES = ["Strategic PM", "Systems Architect", "Product Lead"]

def load_json(path):
    if not os.path.exists(path):
        print(f"Missing file: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def inject_confirmation_chains():
    agents = load_json(AGENTS_PATH)
    agent_by_role = {role: [] for role in CRITICAL_ROLES}
    for agent in agents:
        role = agent.get("role_title")
        name = agent.get("name")
        if role in CRITICAL_ROLES:
            agent_by_role[role].append(name)

    for filename in os.listdir(PACKET_DIR):
        if filename.startswith("real_packet_") and filename.endswith(".json"):
            path = os.path.join(PACKET_DIR, filename)
            packet = load_json(path)
            confirmation_chain = []

            for agent in packet.get("agents", []):
                if agent["role_title"] in CRITICAL_ROLES:
                    confirmation_chain.extend(agent_by_role.get(agent["role_title"], []))

            # Deduplicate and sort
            confirmation_chain = sorted(list(set(confirmation_chain)))
            packet["confirmation_chain"] = confirmation_chain

            with open(path, "w", encoding="utf-8") as f:
                json.dump(packet, f, indent=4)

            print(f"🔐 Injected confirmation chain into {filename}")

    print("✅ All critical roles now require approval before dispatch.")

if __name__ == "__main__":
    inject_confirmation_chains()