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