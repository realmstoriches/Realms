import os
import json
from datetime import datetime
from pathlib import Path

BASE = Path("F:/Realms/realms_core_alpha/agentic_launchpad")
AGENTS = BASE / "agents"
LOGS = BASE / "logs"
OVERSIGHT = BASE / "oversight"
OVERSIGHT.mkdir(exist_ok=True)

def track_agent_uptime():
    report = []
    for script in AGENTS.glob("*.py"):
        name = script.stem.replace("_agent", "").title()
        start = datetime.now()
        result = os.system(f"python {script}")
        end = datetime.now()
        duration = (end - start).total_seconds()
        report.append({
            "agent": name,
            "status": "✅" if result == 0 else "❌",
            "duration_sec": duration
        })

    log_path = OVERSIGHT / f"agent_uptime_{datetime.now().strftime('%Y%m%d')}.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("📋 Agent uptime report generated.")

def monitor_env_integrity():
    required_keys = [
        "AGENTIC_API_KEY", "MAKE_WEBHOOK_URL", "WP_SITE_URL", "WP_USERNAME", "WP_APP_PASSWORD",
        "LINKEDIN_ACCESS_TOKEN", "LINKEDIN_PROFILE_ID", "FACEBOOK_PAGE_ACCESS_TOKEN",
        "FACEBOOK_PAGE_ID", "EMAIL_API_KEY", "EMAIL_SENDER_ADDRESS", "STRIPE_API_KEY"
    ]
    env_path = BASE / ".env"
    with open(env_path, encoding="utf-8") as f:
        lines = f.readlines()
    env = {line.split("=")[0]: line.split("=")[1].strip() for line in lines if "=" in line}
    missing = [key for key in required_keys if key not in env or env[key] in ("", "[empty]")]
    if missing:
        alert_path = OVERSIGHT / f"env_alert_{datetime.now().strftime('%Y%m%d_%H%M')}.log"
        with open(alert_path, "w", encoding="utf-8") as f:
            f.write("⚠️ Missing or empty environment variables:\n")
            for key in missing:
                f.write(f"- {key}\n")
        print(f"🚨 Environment alert: {len(missing)} missing keys logged.")
    else:
        print("✅ Environment integrity check passed.")

def system_health_summary():
    uptime_log = OVERSIGHT / f"agent_uptime_{datetime.now().strftime('%Y%m%d')}.json"
    if not uptime_log.exists():
        print("⚠️ No uptime log found. Run track_agent_uptime() first.")
        return

    with open(uptime_log) as f:
        data = json.load(f)

    total_agents = len(data)
    failed = [a for a in data if a["status"] == "❌"]
    avg_duration = round(sum(a["duration_sec"] for a in data) / total_agents, 2)

    summary = f"""# 🧠 System Health Summary — {datetime.now().strftime('%Y-%m-%d')}

**Total Agents:** {total_agents}  
**Failures:** {len(failed)}  
**Average Execution Time:** {avg_duration} sec

## Failed Agents
"""
    for agent in failed:
        summary += f"- {agent['agent']} ({agent['duration_sec']} sec)\n"

    with open(OVERSIGHT / f"system_health_{datetime.now().strftime('%Y%m%d')}.md", "w", encoding="utf-8") as f:
        f.write(summary)
    print("📊 System health summary generated.")

def main():
    print("🧠 Running oversight master...")
    monitor_env_integrity()
    track_agent_uptime()
    system_health_summary()
    print("✅ Oversight complete. System is resilient and audit-ready.")

if __name__ == "__main__":
    main()