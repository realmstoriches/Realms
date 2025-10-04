import os
import time
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

# === CONFIG ===
WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")  # or any listener endpoint
TOKEN_REFRESH_INTERVAL_HOURS = 4  # how often to refresh
PLATFORMS = {
    "linkedin": {
        "env_key": "LINKEDIN_ACCESS_TOKEN",
        "refresh_url": "https://your-refresh-endpoint.com/linkedin",  # replace with actual
    },
    "facebook": {
        "env_key": "FACEBOOK_ACCESS_TOKEN",
        "refresh_url": "https://your-refresh-endpoint.com/facebook",  # replace with actual
    },
    "wordpress": {
        "env_key": "WORDPRESS_PASSWORD",
        "refresh_url": "https://your-refresh-endpoint.com/wordpress",  # replace with actual
    }
}

# === STATE TRACKING ===
last_refresh = {platform: datetime.utcnow() - timedelta(hours=TOKEN_REFRESH_INTERVAL_HOURS + 1) for platform in PLATFORMS}

def log(msg):
    print(f"{datetime.utcnow().isoformat()} | {msg}")

def refresh_token(platform, config):
    try:
        log(f"🔁 Refreshing token for {platform}")
        res = requests.get(config["refresh_url"])
        res.raise_for_status()
        token = res.json().get("access_token")
        if not token:
            log(f"❌ No token returned for {platform}")
            return False

        payload = {
            "platform": platform,
            "access_token": token
        }
        post = requests.post(WEBHOOK_URL, json=payload)
        post.raise_for_status()
        log(f"✅ Token dispatched for {platform}")
        last_refresh[platform] = datetime.utcnow()
        return True
    except Exception as e:
        log(f"❌ Failed to refresh {platform}: {e}")
        return False

def monitor_and_dispatch():
    log("🧠 Token Dispatch Agent Activated")
    while True:
        for platform, config in PLATFORMS.items():
            elapsed = datetime.utcnow() - last_refresh[platform]
            if elapsed > timedelta(hours=TOKEN_REFRESH_INTERVAL_HOURS):
                refresh_token(platform, config)
        time.sleep(300)  # check every 5 minutes

if __name__ == "__main__":
    monitor_and_dispatch()