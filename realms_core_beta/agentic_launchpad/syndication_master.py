import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'superimage'))
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'superimage'))
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'superimage'))
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'superimage'))
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'superimage'))
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'superimage'))
import json, random, requests
from datetime import datetime
from pathlib import Path
from content_creator import ContentCreator, promptgen



BASE = Path(__file__).resolve().parent.parent
LOGS = BASE / "logs"
ASSETS = BASE / "assets"
QUEUE = LOGS / "post_queue.json"
WEBHOOK = "https://hook.us2.make.com/2u9st81473ley859v4r9ydhyg45jglhw"

for folder in [LOGS, ASSETS]:
    folder.mkdir(parents=True, exist_ok=True)

def generate_post():
    suffix = f"{random.choice(['🚀','🧠','🔥','💡','⚡'])} [{datetime.now().strftime('%H:%M')}]"
    title = generate_text("Generate a high-conversion title for an AI-powered business automation post.")
    raw_body = generate_text(promptgen.generate())
    body = injector(raw_body) + " " + suffix
    creator = ContentCreator()
    filepath = creator.generate_single(title=title, body=body, cta="Join now", output_dir=ASSETS)
    image_url = creator.upload(filepath)
    return {
        "title": title,
        "body": body,
        "cta": "https://buy.stripe.com/6oU8wPbxfcU16UH4wmgfu00",
        "image_url": image_url,
        "video_url": "https://your-video-host.com/intro1.mp4",
        "timestamp": datetime.now().isoformat()
    }

def queue_post():
    post = generate_post()
    queue = []
    if QUEUE.exists():
        queue = json.loads(QUEUE.read_text())
    queue.append(post)
    QUEUE.write_text(json.dumps(queue, indent=2))
    print(f"✅ Queued: {post['title']}")

def dispatch():
    if not QUEUE.exists():
        print("❌ No posts in queue.")
        return
    queue = json.loads(QUEUE.read_text())
    if not queue:
        print("⚠️ Queue is empty.")
        return
    post = queue.pop(0)
    res = requests.post(WEBHOOK, json=post)
    if res.status_code == 200:
        print(f"✅ Dispatched: {post['title']}")
    else:
        print(f"❌ Failed: {res.status_code} → {res.text}")
    QUEUE.write_text(json.dumps(queue, indent=2))

if __name__ == "__main__":
    queue_post()
    dispatch()

def injector():
    return 'Fallback CTA injected'


def send_to_make(payload):
    import requests
    requests.post('https://hook.make.com/your-scenario-id', json=payload)
    print('✅ Sent to Make.com webhook')
