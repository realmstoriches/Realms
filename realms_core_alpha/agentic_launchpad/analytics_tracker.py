import os, json, requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent
MARKETING = BASE / "marketing"
LOGS = BASE / "logs"
ENV_PATH = BASE / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

def track_analytics():
    print("\n📊 Tracking CTA Analytics...")
    calendar_path = MARKETING / "content_calendar.json"
    if not calendar_path.exists():
        print("❌ No content calendar found.")
        return

    with open(calendar_path) as f:
        calendar = json.load(f)
    today = datetime.now().strftime("%Y-%m-%d")
    posts = calendar.get(today, [])

    tracker_url = os.getenv("ANALYTICS_TRACKER_URL")
    if not tracker_url:
        print("❌ ANALYTICS_TRACKER_URL missing in .env")
        return

    for post in posts:
        payload = {
            "platform": post.get("platform", "unknown"),
            "cta": post.get("cta", ""),
            "timestamp": datetime.now().isoformat()
        }
        r = requests.post(tracker_url, json=payload)
        status = "✅" if r.status_code == 200 else "❌"
        print(f"{status} Tracked CTA from {payload['platform']}")

    print("📊 Analytics tracking complete.")

if __name__ == "__main__":
    track_analytics()