import os
import time
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

# === ENV ===
LINKEDIN_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_URN = os.getenv("LINKEDIN_PROFILE_URN")
FACEBOOK_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
WORDPRESS_SITE_URL = os.getenv("WORDPRESS_SITE_URL", "").rstrip("/")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")
WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

POST_TEXT = """🚀 Realms Launches Sovereign Dispatch Engine

Our agentic swarm now syndicates across LinkedIn, Facebook, and WordPress with full fallback logic and timestamped dashboards.

Join the mission → https://realms.ai
"""

def log(platform, status, detail):
    print(f"{datetime.utcnow().isoformat()} | {platform} → {status}: {detail}")

def refresh_token(platform):
    try:
        res = requests.get(f"{WEBHOOK_URL}/{platform}")
        res.raise_for_status()
        token = res.json().get("access_token")
        if platform == "linkedin":
            os.environ["LINKEDIN_ACCESS_TOKEN"] = token
        elif platform == "facebook":
            os.environ["FACEBOOK_ACCESS_TOKEN"] = token
        elif platform == "wordpress":
            os.environ["WORDPRESS_PASSWORD"] = token
        log(platform, "🔁 Token refreshed", "New token received")
        return True
    except Exception as e:
        log(platform, "❌ Token refresh failed", str(e))
        return False

def post_linkedin():
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {os.environ.get('LINKEDIN_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202509"
    }
    payload = {
        "author": LINKEDIN_URN,
        "commentary": POST_TEXT,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 401:
            refresh_token("linkedin")
            return post_linkedin()
        res.raise_for_status()
        log("LinkedIn", "✅ Success", "Post published")
    except Exception as e:
        log("LinkedIn", "❌ Failed", str(e))

def post_facebook():
    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
    payload = {
        "message": POST_TEXT,
        "access_token": os.environ.get("FACEBOOK_ACCESS_TOKEN")
    }
    try:
        res = requests.post(url, data=payload)
        if res.status_code == 403:
            refresh_token("facebook")
            return post_facebook()
        res.raise_for_status()
        log("Facebook", "✅ Success", "Post published")
    except Exception as e:
        log("Facebook", "❌ Failed", str(e))

def post_wordpress():
    url = f"{WORDPRESS_SITE_URL}/wp-json/wp/v2/posts"
    payload = {
        "title": "🚀 Realms Launches Sovereign Dispatch Engine",
        "content": POST_TEXT,
        "status": "publish"
    }
    try:
        res = requests.post(url, json=payload, auth=(WORDPRESS_USERNAME, os.environ.get("WORDPRESS_PASSWORD")))
        if res.status_code == 404:
            log("WordPress", "🔁 Healing", "Malformed endpoint—retrying with corrected URL")
            url = f"{WORDPRESS_SITE_URL.rstrip('/')}/wp-json/wp/v2/posts"
            res = requests.post(url, json=payload, auth=(WORDPRESS_USERNAME, os.environ.get("WORDPRESS_PASSWORD")))
        res.raise_for_status()
        log("WordPress", "✅ Success", "Post published")
    except Exception as e:
        log("WordPress", "❌ Failed", str(e))

def dispatch_loop():
    log("Supervisor", "🧠 Activated", "Beginning autonomous syndication")
    while True:
        post_linkedin()
        post_facebook()
        post_wordpress()
        log("Supervisor", "🕒 Sleeping", "Next dispatch in 6 hours")
        time.sleep(21600)  # 6 hours

if __name__ == "__main__":
    dispatch_loop()