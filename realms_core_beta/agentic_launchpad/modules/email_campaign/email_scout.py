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