import os
import re
import shutil
import json
import logging
import datetime
import subprocess

# === CONFIGURATION ===
ROOT_DIR = r"F:\Realms"
ALPHA_DIR = os.path.join(ROOT_DIR, "realms_core_alpha")
BETA_DIR = os.path.join(ROOT_DIR, "realms_core_beta")
AGENT_POOL = os.path.join(ROOT_DIR, "agentic_pool")
LOG_PATH = os.path.join(ROOT_DIR, "sync_logs", "agent_sync.log")
DASHBOARD_PATH = os.path.join(ROOT_DIR, "agentic_dashboard.json")
REQUIRED_FILES = ["agent.py", "config.json"]
AGENT_SIGNATURES = [r"\bdef\s+run\(", r"\bdef\s+dispatch\(", r"class\s+Agent", r"from\s+agentic_core"]

# === SETUP ===
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
os.makedirs(AGENT_POOL, exist_ok=True)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s - %(message)s')

def log(msg):
    print(msg)
    logging.info(msg)

def scan_for_agents(base_dir):
    agent_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        code = f.read()
                        if any(re.search(sig, code) for sig in AGENT_SIGNATURES):
                            agent_files.append(path)
                except Exception as e:
                    log(f"⚠️ Failed to read {path}: {e}")
    return agent_files

def validate_agent(path):
    agent_dir = os.path.dirname(path)
    return [req for req in REQUIRED_FILES if not os.path.exists(os.path.join(agent_dir, req))]

def repair_agent(agent_path, missing):
    agent_dir = os.path.dirname(agent_path)
    for file in missing:
        if file == "config.json":
            default_config = {
                "agent_name": os.path.basename(agent_dir),
                "version": "1.0",
                "status": "initialized",
                "created": str(datetime.datetime.now())
            }
            with open(os.path.join(agent_dir, "config.json"), "w") as f:
                json.dump(default_config, f, indent=2)
            log(f"🛠️ Repaired config.json in {agent_dir}")
        elif file == "agent.py" and agent_path.endswith("agent.py"):
            with open(agent_path, "w") as f:
                f.write("def run():\n    print('Agent running')\n")
            log(f"🛠️ Stubbed agent.py in {agent_dir}")

def containerize_agent(agent_path):
    agent_dir = os.path.dirname(agent_path)
    agent_name = os.path.basename(agent_dir)
    target_dir = os.path.join(AGENT_POOL, agent_name)
    os.makedirs(target_dir, exist_ok=True)
    for item in os.listdir(agent_dir):
        src = os.path.join(agent_dir, item)
        dst = os.path.join(target_dir, item)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
    log(f"📦 Containerized: {agent_name}")
    return {
        "name": agent_name,
        "path": target_dir,
        "status": "ready",
        "last_synced": str(datetime.datetime.now())
    }

def build_dashboard(agent_records):
    with open(DASHBOARD_PATH, "w") as f:
        json.dump(agent_records, f, indent=2)
    log(f"📊 Dashboard updated: {DASHBOARD_PATH}")

def main():
    log("🚀 Starting full agent discovery and sync...")
    alpha_agents = scan_for_agents(ALPHA_DIR)
    beta_agents = scan_for_agents(BETA_DIR)
    all_agents = list(set(alpha_agents + beta_agents))

    log(f"🧠 Discovered {len(all_agents)} agent files")

    dashboard = []
    for agent_path in all_agents:
        if missing := validate_agent(agent_path):
            repair_agent(agent_path, missing)
        record = containerize_agent(agent_path)
        dashboard.append(record)

    build_dashboard(dashboard)
    log("🎯 All agents validated, repaired, and containerized.")

if __name__ == "__main__":
    main()