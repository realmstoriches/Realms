import os
import time
from datetime import datetime
from pathlib import Path

BASE = Path("F:/Realms/realms_core_alpha/agentic_launchpad")
MODULES = BASE / "modules"
LOGS = BASE / "logs"
LOGS.mkdir(exist_ok=True)
LOG_PATH = LOGS / f"finish_line_{datetime.now().strftime('%Y%m%d_%H%M')}.log"

def run(name, command):
    start = datetime.now()
    result = os.system(command)
    end = datetime.now()
    duration = round((end - start).total_seconds(), 2)
    status = "✅ Success" if result == 0 else "❌ Failed"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{start}] {name} → {status} ({duration}s)\n")
    print(f"{status} | {name} ({duration}s)")
    if result != 0:
        recover(name)

def recover(name):
    fallback = {
        "syndication_engine": f"python {MODULES}/syndication_agent.py",
        "stripe_gateway": f"python {MODULES}/stripe_checkout_agent.py",
        "analytics_master": "python analytics_master.py",
        "oversight_master": "python oversight_master.py"
    }
    if name in fallback:
        print(f"🔁 Recovery triggered for {name}...")
        os.system(fallback[name])
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] Recovery attempted for {name}\n")

def main():
    print("🚀 Final launch sequence initiated...")
    steps = [
        ("agentic_initializer", "python agentic_initializer.py"),
        ("upgrade_master", "python upgrade_master.py"),
        ("orchestration_master", "python orchestration_master.py"),
        ("monetization_master", "python monetization_master.py"),
        ("cta_inserter", f"python {MODULES}/cta_inserter.py"),
        ("syndication_engine", f"python {MODULES}/syndication_engine.py"),
        ("analytics_master", "python analytics_master.py"),
        ("oversight_master", "python oversight_master.py")
    ]
    for name, cmd in steps:
        run(name, cmd)
        time.sleep(2)
    print("🏁 Finish line reached. Logs saved to:", LOG_PATH)

if __name__ == "__main__":
    main()