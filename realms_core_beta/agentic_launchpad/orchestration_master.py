import os
import json
import time
from pathlib import Path
from datetime import datetime

BASE = Path("F:/Realms/realms_core_alpha/agentic_launchpad")
AGENTS = BASE / "agents"
LOGS = BASE / "logs"
ORCHESTRATION = BASE / "orchestration"
ORCHESTRATION.mkdir(exist_ok=True)

def load_agent_manifest():
    manifest_path = BASE / "agent_manifest.yaml"
    if not manifest_path.exists():
        print("⚠️ No agent_manifest.yaml found.")
        return []
    import yaml
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    return manifest.get("agents", [])

def prioritize_agents(agents):
    priority_map = {
        "PresidentAgent": 1,
        "CFOAgent": 2,
        "CTOAgent": 3,
        "CMOAgent": 4,
        "ProductManagerAgent": 5,
        "SoftwareArchitectAgent": 6,
        "SoftwareDeveloperAgent": 7,
        "DevOpsAgent": 8,
        "QAAgent": 9,
        "UIUXDesignerAgent": 10,
        "TechnicalWriterAgent": 11,
        "MarketingContentAgent": 12,
        "SalesAgent": 13,
        "LegalCounselAgent": 14,
        "CustomerSupportAgent": 15
    }
    return sorted(agents, key=lambda a: priority_map.get(a["role"], 99))

def stagger_launch(agents, delay=3):
    log_path = ORCHESTRATION / f"launch_log_{datetime.now().strftime('%Y%m%d_%H%M')}.log"
    with open(log_path, "w", encoding="utf-8") as f:
        for agent in agents:
            script_path = BASE / agent["script"]
            f.write(f"[{datetime.now()}] Launching {agent['role']}...\n")
            print(f"🚀 Launching {agent['role']}...")
            result = os.system(f"python {script_path}")
            status = "✅ Success" if result == 0 else "❌ Failed"
            f.write(f"[{datetime.now()}] {agent['role']} → {status}\n")
            time.sleep(delay)

def main():
    print("🧠 Running orchestration master...")
    agents = load_agent_manifest()
    if not agents:
        print("⚠️ No agents found in manifest.")
        return
    prioritized = prioritize_agents(agents)
    stagger_launch(prioritized)
    print("✅ Crew optimization and staggered launch complete.")

if __name__ == "__main__":
    main()