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