import os, subprocess, json, time
from datetime import datetime

BRIDGE = r"F:\Realms\agentic_bridge"
DASHBOARD = os.path.join(BRIDGE, "..", "agentic_dashboard.json")
LOGS = os.path.join(BRIDGE, "..", "logs")

MODULES = {
    "1": ("Run Orchestrator", "realms_orchestrator.py"),
    "2": ("Dispatch Agents", "dispatch_supervisor.py"),
    "3": ("Monitor Health", "agentic_watchdog.py"),
    "4": ("Track Revenue", "revenue_tracker.py"),
    "5": ("Rotate Credentials", "credential_rotator.py"),
    "6": ("Validate .env File", "env_validator.py"),
    "7": ("Start Dashboard API", "dashboard_api.py"),
    "8": ("Refresh ChromaDB", "chroma_migrator.py")
}

def run_module(script):
    path = os.path.join(BRIDGE, script)
    if not os.path.exists(path):
        print(f"❌ Module not found: {script}")
        return
    subprocess.run(["python", path])

def show_status():
    try:
        with open(DASHBOARD, "r") as f:
            data = json.load(f)
        agents = data.get("agents", [])
        monetization = data.get("monetization", [])
        syndication = data.get("syndication", [])
        print(f"\n🧠 Agent Count: {len(agents)}")
        print(f"💰 Monetization Logs: {len(monetization)}")
        print(f"📡 Syndication Payloads: {len(syndication)}")
        print(f"📦 Last Sync: {data.get('timestamp', '—')}")
    except Exception as e:
        print(f"⚠️ Failed to read dashboard: {e}")

def menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== 🧭 Sovereign Swarm Control Panel ===")
        for key, (desc, _) in MODULES.items():
            print(f"[{key}] {desc}")
        print("[S] Show Status")
        print("[Q] Quit")
        choice = input("\nSelect an option: ").strip().upper()
        if choice == "Q":
            break
        elif choice == "S":
            show_status()
            input("\nPress Enter to return to menu...")
        elif choice in MODULES:
            print(f"\n🚀 Launching: {MODULES[choice][0]}")
            run_module(MODULES[choice][1])
            input("\n✅ Done. Press Enter to return to menu...")
        else:
            print("❌ Invalid choice")
            time.sleep(1)

if __name__ == "__main__":
    menu()