import os

BASE_DIR = "F:/Realms/realms_core_alpha/agentic_launchpad/modules/email_campaign"
os.makedirs(BASE_DIR, exist_ok=True)

def write_agent(filename, content):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"✅ Dropped: {filename}")

write_agent("email_scout_real.py", '''
import csv, json, os

BASE_DIR = os.path.dirname(__file__)
def ensure_file(path): os.makedirs(os.path.dirname(path), exist_ok=True); return path

def scout_emails():
    source_file = os.path.join(BASE_DIR, "leads.csv")
    out_path = ensure_file(os.path.join(BASE_DIR, "email_list_verified.json"))
    emails = []

    if not os.path.exists(source_file):
        print("⚠️ No leads.csv found. Please drop a CSV with 'email' and 'consent' columns.")
        return

    with open(source_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "email" in row and row["email"] and row.get("consent", "true").lower() == "true":
                emails.append({
                    "email": row["email"],
                    "source": row.get("source", "manual import"),
                    "consent": True
                })

    with open(out_path, "w") as f:
        json.dump(emails, f, indent=2)
    print(f"📡 EmailScoutReal: {len(emails)} emails verified and saved.")

if __name__ == "__main__":
    scout_emails()
''')

write_agent("email_verifier_real.py", '''
import json, os, requests

BASE_DIR = os.path.dirname(__file__)
def ensure_file(path): os.makedirs(os.path.dirname(path), exist_ok=True); return path

API_KEY = "your_neverbounce_api_key"  # Replace with your actual key
VERIFY_URL = "https://api.neverbounce.com/v4/single/check"

def verify_emails():
    in_path = os.path.join(BASE_DIR, "email_list_verified.json")
    out_path = ensure_file(os.path.join(BASE_DIR, "email_list_clean.json"))

    if not os.path.exists(in_path):
        print("❌ No verified email list found.")
        return

    with open(in_path, "r") as f:
        raw = json.load(f)

    clean = []
    for entry in raw:
        email = entry["email"]
        try:
            response = requests.get(VERIFY_URL, params={"email": email, "key": API_KEY})
            result = response.json()
            if result.get("result") == "valid":
                clean.append(entry)
                print(f"✅ Valid: {email}")
            else:
                print(f"❌ Invalid: {email} ({result.get('result')})")
        except Exception as e:
            print(f"⚠️ Error verifying {email}: {e}")

    with open(out_path, "w") as f:
        json.dump(clean, f, indent=2)
    print(f"📬 EmailVerifierReal: {len(clean)} emails passed verification.")

if __name__ == "__main__":
    verify_emails()
''')
print("\n📦 Real acquisition and verification modules deployed.")