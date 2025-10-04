import os
import subprocess
agents = [
    r"F:\Realms\\Orchestration\Agents\Agent1",
    r"C:\Users\user\Desktop\Orchestration\Agents\Agent2"
]




def activate_agent(agent_path):
    try:
        subprocess.run(["python", os.path.join(agent_path, "agent.py")])
        print(f"🚀 Activated: {agent_path}")
    except Exception as e:
        print(f"❌ Failed: {agent_path} — {e}")

for agent in agents:
    activate_agent(agent)