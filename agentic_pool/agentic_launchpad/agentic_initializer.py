import os
import json
from pathlib import Path
from datetime import datetime

BASE = Path("F:/Realms/realms_core_alpha/agentic_launchpad")
ENV_PATH = BASE / ".env"
TEMPLATE_PATH = BASE / ".env.template"
BUSINESS = BASE / "business"
MARKETING = BASE / "marketing"
LOGS = BASE / "logs"
MODULES = BASE / "modules"

def load_env():
    if not ENV_PATH.exists():
        ENV_PATH.write_text("")
    with open(".env") as f:
        lines = f.readlines()
    env = {}
    for line in lines:
        if "=" in line:
            key, val = line.strip().split("=", 1)
            env[key] = val
    return env

def load_template():
    with open(".env") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def populate_missing_env():
    env = load_env()
    template = load_template()
    missing = [key for key in template if key not in env]

    # Agentic population logic
    guesses = {
        "MAKE_WEBHOOK_URL": "https://hook.make.com/your-scenario-id",
        "EMAIL_API_KEY": "sk-test-yourkey",
        "EMAIL_SENDER_ADDRESS": "noreply@realmstoriches.xyz",
        "WP_SITE_URL": "https://blog.realmstoriches.xyz",
        "WP_USERNAME": "realms_admin",
        "WP_APP_PASSWORD": "app-password-here",
        "LINKEDIN_ACCESS_TOKEN": "linkedin-access-token",
        "LINKEDIN_PROFILE_ID": "your-profile-id",
        "FACEBOOK_PAGE_ACCESS_TOKEN": "facebook-page-token",
        "FACEBOOK_PAGE_ID": "1234567890",
        "STRIPE_API_KEY": "sk_test_yourstripekey"
    }

    with open(".env", "a") as f:
        for key in missing:
            val = guesses.get(key, "")
            f.write(f"{key}={val}\n")
            print(f"🔧 Populated {key} → {val or '[empty]'}")

def create_content_calendar():
    MARKETING.mkdir(exist_ok=True)
    calendar_path = MARKETING / "content_calendar.json"
    if not calendar_path.exists():
        today = datetime.now().strftime("%Y-%m-%d")
        sample = [{
            "title": "How Agentic Teams Build Sovereignty",
            "body": "Discover how Realms to Riches automates outreach, monetization, and legacy creation using AI-powered crews."
        }]
        with open(calendar_path, "w") as f:
            json.dump({today: sample}, f, indent=2)
        print(f"📝 Created content_calendar.json with sample post for {today}")

def create_agent_manifest():
    manifest = {
        "manifest_version": "1.0",
        "organization": "Realms to Riches",
        "mission": "Build a sovereign, operationally independent outreach and monetization engine that scales globally and preserves founder sovereignty.",
        "agents": []
    }
    with open(BUSINESS / "company_structure.json") as f:
        roles = json.load(f)
        for role in roles:
            manifest["agents"].append({
                "role": role["role_name"],
                "script": f"agents/{role['script']}",
                "responsibilities": role["responsibilities"]
            })
    with open(BASE / "agent_manifest.yaml", "w") as f:
        import yaml
        yaml.dump(manifest, f, sort_keys=False)
    print("📜 Created agent_manifest.yaml")

def create_logs_folder():
    LOGS.mkdir(exist_ok=True)
    print("📁 Logs folder ready")

def main():
    print("🧠 Initializing full system...")
    populate_missing_env()
    create_content_calendar()
    create_agent_manifest()
    create_logs_folder()
    print("✅ Initialization complete. System is ready for autonomous launch.")

if __name__ == "__main__":
    main()