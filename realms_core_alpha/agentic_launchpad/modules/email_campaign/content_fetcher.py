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