import time
import json

LOG_PATH = "control/agent_log.txt"

def log_action(agent_id, task, status):
    entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "agent_id": agent_id,
        "task": task,
        "status": status
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"✅ Logged: {agent_id} | {task} | {status}")

if __name__ == "__main__":
    log_action("agent_001", "dispatch_wordpress", "success")