import json
import random

def simulate_health(agent_count=1000):
    health = []
    for i in range(agent_count):
        agent_id = f"agent_{i+1}"
        status = random.choices(["active", "idle", "error"], weights=[0.85, 0.1, 0.05])[0]
        health.append({"agent_id": agent_id, "status": status})

    with open("logs/agent_health.json", "w") as f:
        json.dump(health, f, indent=2)

    print("✅ Agent health data saved to logs/agent_health.json")

if __name__ == "__main__":
    simulate_health()