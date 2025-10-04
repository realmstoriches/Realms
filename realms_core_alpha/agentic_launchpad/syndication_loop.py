import time, json
from datetime import datetime
from pathlib import Path

LOGS = Path(__file__).resolve().parent / "logs"
DASHBOARD = Path(__file__).resolve().parent / "launch_dashboard.json"
MAX_ATTEMPTS = 5
PLATFORMS = ["LinkedIn", "Twitter", "Facebook"]
STATUS = {p: [] for p in PLATFORMS}

def post_to_platform(platform, payload):
    # Simulated post logic
    if platform == "LinkedIn":
        return False  # simulate failure
    return True

def log_attempt(platform, success):
    STATUS[platform].append({
        "timestamp": datetime.now().isoformat(),
        "success": success
    })

def update_dashboard():
    if DASHBOARD.exists():
        data = json.load(open(DASHBOARD))
    else:
        data = {}
    data["syndication_status"] = {
        "LinkedIn": STATUS["LinkedIn"],
        "Twitter": STATUS["Twitter"],
        "Facebook": STATUS["Facebook"],
        "last_attempt": datetime.now().isoformat(),
        "fallback_triggered": all(not any(s["success"] for s in STATUS[p]) for p in PLATFORMS)
    }
    with open(DASHBOARD, "w") as f:
        json.dump(data, f, indent=2)

def trigger_fallback():
    print("🛡️ Syndication fallback triggered...")
    # Add fallback logic here (e.g., notify, requeue, switch platform)

def main():
    print("🔁 Starting Syndication Loop...")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\n🔄 Attempt {attempt}: Syndicating...")
        for platform in PLATFORMS:
            success = post_to_platform(platform, payload={})
            log_attempt(platform, success)
            print(f"{'✅' if success else '❌'} Syndicated to {platform}")
        if all(any(s["success"] for s in STATUS[p]) for p in PLATFORMS):
            break
        time.sleep(2 * attempt)

    update_dashboard()

    if all(not any(s["success"] for s in STATUS[p]) for p in PLATFORMS):
        trigger_fallback()

    print("✅ Syndication loop complete.")

if __name__ == "__main__":
    main()