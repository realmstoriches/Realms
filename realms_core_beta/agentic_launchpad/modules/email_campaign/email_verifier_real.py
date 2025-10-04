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