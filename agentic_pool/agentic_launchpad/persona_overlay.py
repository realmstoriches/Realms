import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent
MARKETING = BASE / "marketing"
calendar_path = MARKETING / "content_calendar.json"

def overlay_persona():
    print("\n🧬 Applying Persona Overlay...")
    if not calendar_path.exists():
        print("❌ No content calendar found.")
        return

    with open(calendar_path) as f:
        calendar = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    posts = calendar.get(today, [])

    for post in posts:
        if "Realms" in post["body"]:
            post["body"] = post["body"].replace("Realms", "Realms to Riches™")
        post["body"] += "\n\n🧠 Powered by agentic automation."

    calendar[today] = posts
    with open(calendar_path, "w") as f:
        json.dump(calendar, f, indent=2)

    print("✅ Persona overlay applied to today's posts.")

if __name__ == "__main__":
    overlay_persona()