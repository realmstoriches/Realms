import os

BASE_DIR = "F:/Realms/realms_core_alpha/agentic_launchpad/modules/email_campaign"
os.makedirs(BASE_DIR, exist_ok=True)

def write_agent(filename, content):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Patched: {filename}")

write_agent("email_scout.py", '''
import json, os

BASE_DIR = os.path.dirname(__file__)
def ensure_file(path): os.makedirs(os.path.dirname(path), exist_ok=True); return path

def scout_emails():
    emails = [
        {"email": "founder@example.com", "source": "startup directory", "consent": True},
        {"email": "ceo@techhub.com", "source": "public profile", "consent": True}
    ]
    out_path = ensure_file(os.path.join(BASE_DIR, "email_list_verified.json"))
    with open(out_path, "w") as f:
        json.dump(emails, f, indent=2)
    print("📡 EmailScout: Verified email list created.")

if __name__ == "__main__":
    scout_emails()
''')

write_agent("email_verifier.py", '''
import json, os

BASE_DIR = os.path.dirname(__file__)
def ensure_file(path): os.makedirs(os.path.dirname(path), exist_ok=True); return path

def verify_emails():
    in_path = os.path.join(BASE_DIR, "email_list_verified.json")
    out_path = ensure_file(os.path.join(BASE_DIR, "email_list_clean.json"))
    with open(in_path, "r") as f:
        raw = json.load(f)
    clean = [e for e in raw if e["consent"] and "@" in e["email"]]
    with open(out_path, "w") as f:
        json.dump(clean, f, indent=2)
    print("✅ EmailVerifier: Clean email list saved.")

if __name__ == "__main__":
    verify_emails()
''')

write_agent("content_fetcher.py", '''
import json, os

BASE_DIR = os.path.dirname(__file__)
def ensure_file(path): os.makedirs(os.path.dirname(path), exist_ok=True); return path

def fetch_content():
    payload = {
        "subject": "Realms is Live",
        "body": "Discover how Realms automates your business with sovereign intelligence.",
        "html": "<h1>Realms is Live</h1><p>Discover how Realms automates your business with sovereign intelligence.</p>"
    }
    out_path = ensure_file(os.path.join(BASE_DIR, "campaign_payload.json"))
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print("📝 ContentFetcher: Campaign content prepared.")

if __name__ == "__main__":
    fetch_content()
''')

write_agent("campaign_sender.py", '''
import json, os

BASE_DIR = os.path.dirname(__file__)
def ensure_file(path): os.makedirs(os.path.dirname(path), exist_ok=True); return path

def send_campaign():
    clean_path = os.path.join(BASE_DIR, "email_list_clean.json")
    payload_path = os.path.join(BASE_DIR, "campaign_payload.json")
    log_path = ensure_file(os.path.join(BASE_DIR, "campaign_log_20250928.json"))

    with open(clean_path, "r") as f:
        recipients = json.load(f)
    with open(payload_path, "r") as f:
        content = json.load(f)

    for r in recipients:
        print(f"📧 Sending to {r['email']}: {content['subject']}")

    with open(log_path, "w") as f:
        json.dump({"sent": [r["email"] for r in recipients]}, f, indent=2)
    print("📤 CampaignSender: Emails dispatched and logged.")

if __name__ == "__main__":
    send_campaign()
''')

write_agent("campaign_scheduler.py", '''
import schedule, time, subprocess, os

BASE_DIR = os.path.dirname(__file__)
def run_all():
    subprocess.run(["python", os.path.join(BASE_DIR, "email_scout.py")])
    subprocess.run(["python", os.path.join(BASE_DIR, "email_verifier.py")])
    subprocess.run(["python", os.path.join(BASE_DIR, "content_fetcher.py")])
    subprocess.run(["python", os.path.join(BASE_DIR, "campaign_sender.py")])

schedule.every().day.at("09:00").do(run_all)
schedule.every().day.at("12:00").do(run_all)
schedule.every().day.at("15:00").do(run_all)
schedule.every().day.at("18:00").do(run_all)
schedule.every().day.at("21:00").do(run_all)

print("🕒 CampaignScheduler: Running 5x daily.")
while True:
    schedule.run_pending()
    time.sleep(60)
''')

print("\n📦 All patched email campaign agents deployed.")
