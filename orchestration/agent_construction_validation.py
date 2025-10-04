import os
import json
import sys
import subprocess

from pathlib import Path
from orchestration.agent_discovery import discover_agents
agents = discover_agents()
print("Found agents:", ", ".join(agents))


REQUIRED_FILES = ["agent.py", "config.json"]

def validate_agent(agent_path):
    missing = [file for file in REQUIRED_FILES if not os.path.exists(os.path.join(agent_path, file))]
    try:
        subprocess.check_output(["python", os.path.join(agent_path, "agent.py"), "--validate"], stderr=subprocess.STDOUT)
        return True, missing
    except Exception as e:
        return False, missing

for agent in agents:
    valid, missing = validate_agent(agent)
    status = "✅ VALID" if valid and not missing else "⚠️ INVALID"
    print(f"{status}: {agent} {'(missing: ' + ', '.join(missing) + ')' if missing else ''}")