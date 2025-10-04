import os
from pathlib import Path

BASE = Path(__file__).parent.parent
AGENTS = BASE / "agents"

def monitor_agents():
    for script in AGENTS.glob("*.py"):
        result = os.system(f"python {script}")
        if result != 0:
            print(f"⚠️ Agent {script.name} failed. Retrying...")
            os.system(f"python {script}")

if __name__ == "__main__":
    monitor_agents()
