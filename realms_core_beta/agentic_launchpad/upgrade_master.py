import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

BASE = Path("F:/Realms/realms_core_alpha/agentic_launchpad")
MODULES = BASE / "modules"
LOGS = BASE / "logs"
BUSINESS = BASE / "business"
MARKETING = BASE / "marketing"

def ensure_modules():
    MODULES.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)

def create_syndication_agent():
    code = """import os
import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent.parent
LOGS = BASE / "logs"
MARKETING = BASE / "marketing"
CALENDAR = MARKETING / "content_calendar.json"

def check_logs():
    today = datetime.now().strftime("%Y%m%d")
    log_path = LOGS / f"syndication_{today}.log"
    if not log_path.exists():
        print("⚠️ No syndication log found. Triggering fallback.")
        os.system("python modules/syndication_engine.py")
    else:
        print("✅ Syndication already completed today.")

def schedule_next():
    tomorrow = (datetime.now().date()).strftime("%Y-%m-%d")
    with open(CALENDAR, "r+") as f:
        data = json.load(f)
        if tomorrow not in data:
            data[tomorrow] = [{
                "title": "Why Agentic Systems Outperform Traditional Teams",
                "body": "Explore how Realms to Riches scales outreach and monetization with modular AI crews."
            }]
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
            print(f"📆 Scheduled content for {tomorrow}")

if __name__ == "__main__":
    check_logs()
    schedule_next()
"""
    (MODULES / "syndication_agent.py").write_text(code, encoding="utf-8")

def create_stripe_gateway():
    code = """import os
from agentic_launchpad.config_manager import get_env

def activate_gateway():
    key = get_env("STRIPE_API_KEY")
    if not key or key == "[empty]":
        print("⚠️ Stripe API key missing. Monetization paused.")
    else:
        print(f"✅ Stripe gateway activated with key: {key[:6]}...")

if __name__ == "__main__":
    activate_gateway()
"""
    (MODULES / "stripe_gateway.py").write_text(code, encoding="utf-8")

def create_pitch_deck_generator():
    code = """import json
from pathlib import Path

BASE = Path(__file__).parent.parent
PLAN = BASE / "business" / "business_plan.json"
DECK = BASE / "business" / "investor_pitch_deck.md"

def generate_deck():
    with open(PLAN) as f:
        plan = json.load(f)
    md = f\"\"\"# Investor Pitch Deck

## Brand
{plan['brand']}

## Mission
{plan['mission']}

## Market Opportunity
Themes: {', '.join(plan['content_strategy']['themes'])}
Channels: {', '.join(plan['content_strategy']['channels'])}

## Product
Agentic automation platform for outreach, monetization, and legacy creation.

## Monetization
Methods: {', '.join(plan['monetization']['methods'])}
CTA: {plan['monetization']['cta']}

## Infrastructure
Blog: {plan['infrastructure']['blog_subdomain']}
Host: {plan['infrastructure']['host']}

## Automation
Platform: {plan['automation']['platform']}
Trigger: {plan['automation']['trigger']}
\"\"\"
    with open(DECK, "w") as f:
        f.write(md)
    print("📊 Investor pitch deck generated.")

if __name__ == "__main__":
    generate_deck()
"""
    (MODULES / "investor_pitch_deck_generator.py").write_text(code, encoding="utf-8")

def create_fallback_monitor():
    code = """import os
from pathlib import Path

BASE = Path(__file__).parent.parent
AGENTS = BASE / "agents"

def monitor_agents():
    for script in AGENTS.glob("*.py"):
        result = os.system(f"python {script}")
        if result != 0:
            print(f"⚠️ Agent {script.name} failed. Retrying...")
            os.system(f"python {script}")

if __name__ == "__main__":
    monitor_agents()
"""
    (MODULES / "fallback_monitor.py").write_text(code, encoding="utf-8")

def create_scheduler_batch():
    code = """@echo off
cd /d F:\\Realms\\realms_core_alpha\\agentic_launchpad
python agentic_autopilot.py
python modules/syndication_agent.py
"""
    (BASE / "daily_scheduler.bat").write_text(code)
    print("📅 Created daily_scheduler.bat for Task Scheduler")

def main():
    print("🧠 Running upgrade master...")
    ensure_modules()
    create_syndication_agent()
    create_stripe_gateway()
    create_pitch_deck_generator()
    create_fallback_monitor()
    create_scheduler_batch()
    print("✅ All upgrades deployed. System is now fully autonomous and investor-ready.")

if __name__ == "__main__":
    main()