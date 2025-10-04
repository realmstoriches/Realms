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