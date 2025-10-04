import os

ALPHA_PATH = r"F:\Realms\realms_core_alpha"

def discover_agents():
    agents = []
    for item in os.listdir(ALPHA_PATH):
        path = os.path.join(ALPHA_PATH, item)
        if os.path.isdir(path) or item.endswith(".py"):
            agents.append(path)
    return agents

if __name__ == "__main__":
    agents = discover_agents()
    print(f"🧠 Discovered {len(agents)} agents:")
    for agent in agents:
        print(f" - {agent}")