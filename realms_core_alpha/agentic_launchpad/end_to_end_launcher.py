import os
import time
from datetime import datetime
from pathlib import Path

BASE = Path("F:/Realms/realms_core_alpha/agentic_launchpad")
MODULES = BASE / "modules"
LOGS = BASE / "logs"
LAUNCH_LOG = LOGS / f"end_to_end_{datetime.now().strftime('%Y%m%d_%H%M')}.log"

def run_step(name, command):
    start = datetime.now()
    result = os.system(command)
    end = datetime.now()
    duration = round((end - start).total_seconds(), 2)
    status = "✅ Success" if result == 0 else "❌ Failed"
    with open(LAUNCH_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{start}] {name} → {status} ({duration}s)\n")
    print(f"{status} | {name} ({duration}s)")
    if result != 0:
        recover(name)

def recover(name):
    fallback = {
        "agentic_autopilot": "python modules/fallback_monitor.py",
        "syndication_engine": "python modules/syndication_agent.py",
        "stripe_gateway": "python modules/stripe_gateway.py",
        "analytics_master": "python analytics_master.py",
        "oversight_master": "python oversight_master.py"
    }
    if name in fallback:
        print(f"🔁 Attempting recovery for {name}...")
        os.system(fallback[name])
        with open(LAUNCH_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] Recovery triggered for {name}\n")

def main():
    print("🚀 Starting full end-to-end launch...")
    steps = [
        ("agentic_initializer", "python agentic_initializer.py"),
        ("upgrade_master", "python upgrade_master.py"),
        ("orchestration_master", "python orchestration_master.py"),
        ("syndication_engine", "python modules/syndication_engine.py"),
        ("stripe_gateway", "python modules/stripe_gateway.py"),
        ("analytics_master", "python analytics_master.py"),
        ("oversight_master", "python oversight_master.py")
    ]
    for name, cmd in steps:
        run_step(name, cmd)
        time.sleep(2)
    print("✅ Full launch complete. Logs saved to:", LAUNCH_LOG)

if __name__ == "__main__":
    main()