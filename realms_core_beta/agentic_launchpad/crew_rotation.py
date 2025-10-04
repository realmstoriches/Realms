import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent
LOGS = BASE / "logs"
MANIFEST = BASE / "agent_manifest.yaml"

def rotate_crew():
    print("\n🔁 Running Crew Rotation Check...")
    log_files = sorted(LOGS.glob("master_log_*.log"), reverse=True)
    if not log_files:
        print("❌ No logs found.")
        return

    with open(log_files[0], encoding="utf-8") as f:
        lines = f.readlines()

    uptime = sum(1 for l in lines if "[SUCCESS]" in l)
    fallback = sum(1 for l in lines if "[FALLBACK]" in l)
    errors = sum(1 for l in lines if "[ERROR]" in l)

    report = {
        "last_log": log_files[0].name,
        "agent_uptime": uptime,
        "fallback_triggered": fallback,
        "errors_detected": errors,
        "rotation_recommended": fallback > 0 or errors > 2
    }

    print("✅ Crew Rotation Report:")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    rotate_crew()