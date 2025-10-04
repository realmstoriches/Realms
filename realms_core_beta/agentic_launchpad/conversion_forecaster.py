import json
from pathlib import Path
from datetime import datetime, timedelta

BASE = Path(__file__).resolve().parent
LOGS = BASE / "logs"
MARKETING = BASE / "marketing"

def forecast():
    print("\n🔮 Running Conversion Forecast...")
    links_path = LOGS / "payment_links.json"
    calendar_path = MARKETING / "content_calendar.json"

    links = json.load(open(links_path)) if links_path.exists() else []
    calendar = json.load(open(calendar_path)) if calendar_path.exists() else {}

    latest_link = links[-1]["url"] if links else "None"
    link_time = datetime.fromisoformat(links[-1]["timestamp"]) if links else datetime.now()
    posts_today = calendar.get(datetime.now().strftime("%Y-%m-%d"), [])

    forecast = {
        "latest_stripe_link": latest_link,
        "posts_today": len(posts_today),
        "cta_injected": sum(1 for p in posts_today if "cta" in p),
        "estimated_clicks": len(posts_today) * 3,
        "conversion_rate": "2–5%",
        "estimated_transactions": round(len(posts_today) * 3 * 0.03),
        "first_transaction_window": f"{(link_time + timedelta(days=1)).strftime('%Y-%m-%d')} to {(link_time + timedelta(days=3)).strftime('%Y-%m-%d')}",
        "stripe_payout_window": f"{(link_time + timedelta(days=3)).strftime('%Y-%m-%d')} to {(link_time + timedelta(days=10)).strftime('%Y-%m-%d')}"
    }

    print("✅ Forecast Complete:")
    print(json.dumps(forecast, indent=2))

if __name__ == "__main__":
    forecast()