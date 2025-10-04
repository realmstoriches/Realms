import os
import requests
import datetime
from dotenv import load_dotenv

# === CONFIGURATION ===
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

LINKEDIN_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
FACEBOOK_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
WORDPRESS_SITE = os.getenv("WORDPRESS_SITE_URL")
WORDPRESS_USER = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASS = os.getenv("WORDPRESS_PASSWORD")

# === AGENT-GENERATED PAYLOAD ===
def generate_payload():
    return {
        "title": "🚀 Realms Launches Sovereign Dispatch Engine",
        "body": "Our agentic swarm now syndicates across LinkedIn, Facebook, and WordPress with full fallback logic and timestamped dashboards.",
        "cta": "Join the mission → https://realms.ai",
        "media_url": "https://realms.ai/assets/launch_video.mp4",  # Replace with agent-generated asset
        "image_url": "https://realms.ai/assets/launch_banner.png"  # Replace with agent-generated asset
    }

# === LINKEDIN DISPATCH ===
def dispatch_linkedin(payload):
    try:
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {LINKEDIN_TOKEN}",
            "Content-Type": "application/json"
        }
        body = {
            "author": f"urn:li:person:{os.getenv('LINKEDIN_PROFILE_URN')}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": f"{payload['title']}\n\n{payload['body']}\n\n{payload['cta']}"},
                    "shareMediaCategory": "VIDEO",
                    "media": [{
                        "status": "READY",
                        "originalUrl": payload["media_url"],
                        "title": {"text": payload["title"]}
                    }]
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        res = requests.post(post_url, headers=headers, json=body)
        res.raise_for_status()
        return {"platform": "LinkedIn", "status": "✅ Success", "timestamp": datetime.datetime.now().isoformat()}
    except Exception as e:
        return agentic_fallback("LinkedIn", str(e))

# === FACEBOOK DISPATCH ===
def dispatch_facebook(payload):
    try:
        post_url = f"https://graph.facebook.com/v18.0/875761185609852/feed"
        params = {
            "message": f"{payload['title']}\n\n{payload['body']}\n\n{payload['cta']}",
            "access_token": FACEBOOK_TOKEN
        }
        res = requests.post(post_url, params=params)
        res.raise_for_status()
        return {"platform": "Facebook", "status": "✅ Success", "timestamp": datetime.datetime.now().isoformat()}
    except Exception as e:
        return agentic_fallback("Facebook", str(e))

# === WORDPRESS DISPATCH ===
def dispatch_wordpress(payload):
    try:
        post_url = f"{WORDPRESS_SITE}/wp-json/wp/v2/posts"
        auth = (WORDPRESS_USER, WORDPRESS_PASS)
        body = {
            "title": payload["title"],
            "content": f"{payload['body']}<br><a href='{payload['cta']}' class='wp-block-button__link'>Join the mission</a>",
            "status": "publish"
        }
        res = requests.post(post_url, auth=auth, json=body)
        res.raise_for_status()
        return {"platform": "WordPress", "status": "✅ Success", "timestamp": datetime.datetime.now().isoformat()}
    except Exception as e:
        return agentic_fallback("WordPress", str(e))

# === AGENTIC FALLBACK ===
def agentic_fallback(platform, error):
    print(f"⚠️ Fallback triggered for {platform}: {error}")
    # Retry logic or queue for later dispatch
    return {"platform": platform, "status": f"❌ Failed: {error}", "timestamp": datetime.datetime.now().isoformat()}

# === DASHBOARD ===
def dispatch_all():
    payload = generate_payload()
    results = [
        dispatch_linkedin(payload),
        dispatch_facebook(payload),
        dispatch_wordpress(payload)
    ]
    print("\n📊 Syndication Dashboard")
    for result in results:
        print(f"{result['timestamp']} | {result['platform']} → {result['status']}")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    dispatch_all()