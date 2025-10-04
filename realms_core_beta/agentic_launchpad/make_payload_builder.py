import json
from pathlib import Path
from datetime import datetime
import random
import string

BASE = Path(__file__).resolve().parent
MARKETING = BASE / "marketing"
LOGS = BASE / "logs"
payload_path = LOGS / "make_payload.json"

def random_suffix(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def build_payload():
    print("\n🧠 Building Make.com Payload...")
    today = datetime.now().strftime("%Y-%m-%d")
    calendar_path = MARKETING / "content_calendar.json"

    if not calendar_path.exists():
        print("❌ No content calendar found.")
        return

    with open(calendar_path) as f:
        calendar = json.load(f)

    posts = calendar.get(today, [])
    if not posts:
        print("❌ No posts found for today.")
        return

    payloads = []
    for post in posts:
        content = post.get("body", "").strip()
        link = post.get("cta", "").strip()

        if not content:
            print("⚠️ Skipping post with empty content.")
            continue

        # Add suffix to avoid LinkedIn duplication
        content += f" 🚀 {random_suffix()}"

        payload = {
            "content": content,
            "commentary": content,
            "link": link
        }
        payloads.append(payload)

    with open(payload_path, "w") as f:
        json.dump(payloads, f, indent=2)

    print(f"✅ Payloads saved to {payload_path.name}")
    print(json.dumps(payloads, indent=2))

if __name__ == "__main__":
    build_payload()