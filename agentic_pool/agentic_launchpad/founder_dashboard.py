import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent
LOGS = BASE / "logs"
DASHBOARD = BASE / "dashboard"
MARKETING = BASE / "marketing"

def load(path):
    return json.load(open(path)) if path.exists() else {}

def build_founder_dashboard():
    print("\n🧾 Building Founder Dashboard...")
    launch = load(DASHBOARD / "launch_dashboard.json")
    forecast = load(DASHBOARD / "conversion_forecast.json")
    calendar = load(MARKETING / "content_calendar.json")

    today = datetime.now().strftime("%Y-%m-%d")
    posts = calendar.get(today, [])

    dashboard = {
        "system_status": {
            "agents_online": launch.get("agents", {}).get("manifest_loaded", False),
            "monetization_active": True,
            "cta_injected": launch.get("cta_status", {}).get("cta_injected", 0),
            "syndication_status": launch.get("forecast", {}).get("syndication_triggered", "Pending")
        },
        "reach": {
            "posts_today": len(posts),
            "estimated_clicks": forecast.get("estimated_clicks", 0),
            "conversion_rate": forecast.get("conversion_rate", "2–5%"),
            "estimated_transactions": forecast.get("estimated_transactions", 0)
        },
        "timeline": {
            "first_transaction_window": forecast.get("first_transaction_window", "Unknown"),
            "stripe_payout_window": forecast.get("stripe_payout_window", "Unknown")
        },
        "stripe_link": forecast.get("latest_stripe_link", "None")
    }

    with open(DASHBOARD / "founder_dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    print("✅ Founder Dashboard saved to founder_dashboard.json")
    print(json.dumps(dashboard, indent=2))

if __name__ == "__main__":
    build_founder_dashboard()