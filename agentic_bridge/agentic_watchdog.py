import json, os
from datetime import datetime

DASHBOARD = r"F:\Realms\agentic_dashboard.json"
LOG = r"F:\Realms\logs\watchdog_log.txt"

def check_agent(agent):
    path = os.path.join(agent["container_path"], "agent.py")
    if not os.path.exists(path):
        return "missing"
    try:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        if "def run(" not in code and "def dispatch(" not in code:
            return "invalid"
        return "healthy"
    except Exception:
        return "unreadable"

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")
    print(msg)

def run():
    with open(DASHBOARD, "r") as f:
        data = json.load(f)
    for agent in data["agents"]:
        status = check_agent(agent)
        agent["health"] = status
        log(f"{agent['name']} → {status}")
    with open(DASHBOARD, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    run()