import os, json, importlib.util

BRIDGE = r"F:\Realms\agentic_bridge"
DASHBOARD = os.path.join(BRIDGE, "..", "agentic_dashboard.json")
REQUIRED_MODULES = [
    "apscheduler", "flask", "tkinter", "chromadb", "ast", "subprocess", "json", "datetime"
]
REQUIRED_SCRIPTS = [
    "realms_orchestrator.py", "dispatch_supervisor.py", "agentic_watchdog.py",
    "revenue_tracker.py", "credential_rotator.py", "dashboard_api.py",
    "env_validator.py", "swarm_scheduler.py", "swarm_webhook.py",
    "swarm_gui.py", "swarm_daemon.py"
]

def check_modules():
    return [mod for mod in REQUIRED_MODULES if importlib.util.find_spec(mod) is None]

def check_scripts():
    return [script for script in REQUIRED_SCRIPTS if not os.path.exists(os.path.join(BRIDGE, script))]

def check_dashboard():
    try:
        with open(DASHBOARD, "r") as f:
            json.load(f)
        return True
    except Exception:
        return False

def run():
    print("🔍 Running full system diagnostic...")
    missing_mods = check_modules()
    missing_scripts = check_scripts()
    dashboard_ok = check_dashboard()

    print(f"\n📦 Missing Modules: {missing_mods if missing_mods else 'None'}")
    print(f"📁 Missing Scripts: {missing_scripts if missing_scripts else 'None'}")
    print(f"📊 Dashboard Integrity: {'✅ OK' if dashboard_ok else '❌ Broken'}")

if __name__ == "__main__":
    run()