import json, subprocess, time
from datetime import datetime

DASHBOARD = r"F:\Realms\agentic_dashboard.json"
LOG = r"F:\Realms\logs\dispatch_log.txt"

def dispatch(agent):
    try:
        subprocess.run(["python", f"{agent['container_path']}\\agent.py"])
        log(f"✅ Dispatched {agent['name']}")
    except Exception as e:
        log(f"❌ Dispatch failed for {agent['name']}: {e}")

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")
    print(msg)

def run(mode="manual"):
    with open(DASHBOARD, "r") as f:
        data = json.load(f)
    agents = data["agents"]

    for agent in agents:
        if mode == "manual" or agent.get("status") == "ready":
            dispatch(agent)

if __name__ == "__main__":
    run(mode="manual")