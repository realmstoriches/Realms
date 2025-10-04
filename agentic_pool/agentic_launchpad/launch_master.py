import subprocess
from pathlib import Path
import time

BASE = Path(__file__).resolve().parent
CHAIN = [
    "config_manager.py",
    "upgrade_master.py",
    "monetization_manager.py",
    "launch_chain.py",
    "syndication_master.py",
    "dashboard_builder.py",
    "realms_autopilot.py"
]

FALLBACK = "fallback_trigger.py"
MAX_RETRIES = 3
FAILED = []

def run_script(script_name):
    script_path = BASE / script_name
    if not script_path.exists():
        print(f"❌ Missing: {script_name}")
        FAILED.append(script_name)
        return False

    print(f"\n🚀 Running: {script_name}")
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            subprocess.run(["python", str(script_path)], check=True)
            print(f"✅ Completed: {script_name}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Attempt {attempt} failed: {script_name}")
            time.sleep(2)  # brief pause before retry
    FAILED.append(script_name)
    return False

def trigger_fallback():
    fallback_path = BASE / FALLBACK
    if not fallback_path.exists():
        print("⚠️ Fallback module missing.")
        return
    print("\n🛡️ Triggering fallback recovery...")
    try:
        subprocess.run(["python", str(fallback_path)], check=True)
        print("✅ Fallback recovery complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Fallback failed: {e}")

def launch_all():
    print("\n🧠 Starting full Realms launch chain...")
    for script in CHAIN:
        run_script(script)

    if FAILED:
        print(f"\n⚠️ Modules failed after retries: {FAILED}")
        trigger_fallback()
    else:
        print("\n✅ All modules completed successfully.")

if __name__ == "__main__":
    launch_all()
