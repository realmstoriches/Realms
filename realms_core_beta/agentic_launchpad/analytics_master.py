import os
import json
from datetime import datetime
from pathlib import Path

BASE = Path("F:/Realms/realms_core_alpha/agentic_launchpad")
LOGS = BASE / "logs"
MARKETING = BASE / "marketing"
DASHBOARD = BASE / "dashboard"
DASHBOARD.mkdir(exist_ok=True)

def track_conversions():
    # Simulated conversion log
    conversions = [
        {"source": "LinkedIn", "clicks": 42, "leads": 8},
        {"source": "Facebook", "clicks": 67, "leads": 12},
        {"source": "Email", "clicks": 31, "leads": 5},
        {"source": "Blog", "clicks": 90, "leads": 20}
    ]
    log_path = LOGS / f"conversions_{datetime.now().strftime('%Y%m%d')}.json"
    with open(log_path, "w") as f:
        json.dump(conversions, f, indent=2)
    print("📈 Conversion data logged.")

def generate_dashboard():
    today = datetime.now().strftime('%Y%m%d')
    log_path = LOGS / f"conversions_{today}.json"
    if not log_path.exists():
        print("⚠️ No conversion log found. Run track_conversions() first.")
        return

    with open(log_path) as f:
        data = json.load(f)

    total_clicks = sum(item["clicks"] for item in data)
    total_leads = sum(item["leads"] for item in data)
    lead_rate = round((total_leads / total_clicks) * 100, 2) if total_clicks else 0

    dashboard_md = f"""# 📊 Realms Performance Dashboard — {today}

**Total Clicks:** {total_clicks}  
**Total Leads:** {total_leads}  
**Lead Conversion Rate:** {lead_rate}%

## Source Breakdown
"""
    for item in data:
        rate = round((item["leads"] / item["clicks"]) * 100, 2) if item["clicks"] else 0
        dashboard_md += f"- **{item['source']}** → {item['clicks']} clicks, {item['leads']} leads ({rate}%)\n"

    with open(DASHBOARD / f"dashboard_{today}.md", "w", encoding="utf-8") as f:
        f.write(dashboard_md)
    print("📊 Dashboard generated.")

def main():
    print("🧠 Running analytics master...")
    track_conversions()
    generate_dashboard()
    print("✅ Analytics and dashboard ready.")

if __name__ == "__main__":
    main()