import os
import requests
from datetime import datetime
from dotenv import load_dotenv

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

# === ENV VARIABLES ===
LINKEDIN_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_URN = os.getenv("LINKEDIN_PROFILE_URN")
FACEBOOK_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
WORDPRESS_SITE_URL = os.getenv("WORDPRESS_SITE_URL", "").rstrip("/")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")

# === POST CONTENT ===
POST_TEXT = """🚀 Realms Launches Sovereign Dispatch Engine

Our agentic swarm now syndicates across LinkedIn, Facebook, and WordPress with full fallback logic and timestamped dashboards.

Join the mission → https://realms.ai
"""

def log_result(platform, status, detail):
    timestamp = datetime.utcnow().isoformat()
    print(f"{timestamp} | {platform} → {status}: {detail}")

# === LINKEDIN ===
def post_linkedin():
    if not LINKEDIN_TOKEN or not LINKEDIN_URN:
        log_result("LinkedIn", "❌ Skipped", "Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_PROFILE_URN")
        return

    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
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
            log_result("LinkedIn", "❌ Failed", "Unauthorized—token may be expired or invalid")
        elif res.status_code == 400:
            log_result("LinkedIn", "❌ Failed", "Bad Request—check URN format and payload structure")
        else:
            res.raise_for_status()
            log_result("LinkedIn", "✅ Success", "Post published")
    except Exception as e:
        log_result("LinkedIn", "❌ Failed", str(e))

# === FACEBOOK ===
def post_facebook():
    if not FACEBOOK_TOKEN or not FACEBOOK_PAGE_ID:
        log_result("Facebook", "❌ Skipped", "Missing FACEBOOK_ACCESS_TOKEN or FACEBOOK_PAGE_ID")
        return

    url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
    payload = {
        "message": POST_TEXT,
        "access_token": FACEBOOK_TOKEN
    }

    try:
        res = requests.post(url, data=payload)
        if res.status_code == 403:
            log_result("Facebook", "❌ Failed", "Forbidden—token lacks permission or is expired")
        else:
            res.raise_for_status()
            log_result("Facebook", "✅ Success", "Post published")
    except Exception as e:
        log_result("Facebook", "❌ Failed", str(e))

# === WORDPRESS ===
def post_wordpress():
    if not WORDPRESS_SITE_URL or not WORDPRESS_USERNAME or not WORDPRESS_PASSWORD:
        log_result("WordPress", "❌ Skipped", "Missing WORDPRESS_SITE_URL, WORDPRESS_USERNAME, or WORDPRESS_PASSWORD")
        return

    url = f"{WORDPRESS_SITE_URL}/wp-json/wp/v2/posts"
    payload = {
        "title": "🚀 Realms Launches Sovereign Dispatch Engine",
        "content": POST_TEXT,
        "status": "publish"
    }

    try:
        res = requests.post(url, json=payload, auth=(WORDPRESS_USERNAME, WORDPRESS_PASSWORD))
        if res.status_code == 404:
            log_result("WordPress", "❌ Failed", "Not Found—check site URL and endpoint structure")
        else:
            res.raise_for_status()
            log_result("WordPress", "✅ Success", "Post published")
    except Exception as e:
        log_result("WordPress", "❌ Failed", str(e))

# === RUN ALL ===
if __name__ == "__main__":
    print("📡 Initiating Sovereign Syndication...\n")
    post_linkedin()
    post_facebook()
    post_wordpress()