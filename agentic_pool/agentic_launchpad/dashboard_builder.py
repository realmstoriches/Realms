import os, json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent
LOGS = BASE / "logs"
MARKETING = BASE / "marketing"
DASHBOARD = BASE / "dashboard"
DASHBOARD.mkdir(exist_ok=True)

def load_json(path):
    return json.load(open(path)) if path.exists() else {}

def build_dashboard():
    print("\n📊 Building Real-Time Dashboard...")
    dashboard = {}

    # Stripe Payment Links
    links_path = LOGS / "payment_links.json"
    links = load_json(links_path)
    dashboard["payment_links"] = {
        "count": len(links),
        "latest": links[-1]["url"] if links else "None"
    }

    # CTA Injection
    calendar_path = MARKETING / "content_calendar.json"
    calendar = load_json(calendar_path)
    today = datetime.now().strftime("%Y-%m-%d")
    posts = calendar.get(today, [])
    dashboard["cta_status"] = {
        "posts_today": len(posts),
        "cta_injected": sum(1 for p in posts if "cta" in p)
    }

    # Agent Manifest
    manifest_path = BASE / "agent_manifest.yaml"
    dashboard["agents"] = {
        "manifest_loaded": manifest_path.exists(),
        "active_roles": "Loaded" if manifest_path.exists() else "Missing"
    }

    # Log Summary
    logs = sorted(LOGS.glob("master_log_*.log"), reverse=True)
    if logs:
        with open(logs[0], encoding="utf-8") as f:
            lines = f.readlines()
        dashboard["log_summary"] = {
            "last_run": logs[0].name,
            "errors": sum(1 for l in lines if "[ERROR]" in l or "[FATAL]" in l),
            "recoveries": sum(1 for l in lines if "[RECOVERY]" in l),
            "successes": sum(1 for l in lines if "[SUCCESS]" in l)
        }

    # Forecast
    dashboard["forecast"] = {
        "estimated_first_transaction": "Within 48 hours",
        "syndication_triggered": "Pending",
        "revenue_window": "2–7 days post-transaction"
    }

    # Save dashboard
    dash_path = DASHBOARD / "launch_dashboard.json"
    with open(dash_path, "w") as f:
        json.dump(dashboard, f, indent=2)
    print("✅ Dashboard built and saved to launch_dashboard.json")
    print(json.dumps(dashboard, indent=2))

if __name__ == "__main__":
    build_dashboard()