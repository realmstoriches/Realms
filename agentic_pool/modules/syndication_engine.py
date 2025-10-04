import os
import json
import requests
from datetime import datetime
from pathlib import Path
import sys

# Ensure config_manager is accessible
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config_manager import get_env

BASE = Path(__file__).resolve().parent.parent
MARKETING = BASE / "marketing"
LOGS = BASE / "logs"
LOGS.mkdir(exist_ok=True)

def load_content():
    with open(MARKETING / "content_calendar.json") as f:
        calendar = json.load(f)
    today = datetime.now().strftime("%Y-%m-%d")
    return calendar.get(today, [])

def push_to_wordpress(post):
    url = get_env("WP_SITE_URL") + "/wp-json/wp/v2/posts"
    auth = (get_env("WP_USERNAME"), get_env("WP_APP_PASSWORD"))
    data = {
        "title": post["title"],
        "content": post["body"],
        "status": "publish"
    }
    r = requests.post(url, auth=auth, json=data)
    return r.status_code == 201

def push_to_linkedin(post):
    token = get_env("LINKEDIN_ACCESS_TOKEN")
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "author": f"urn:li:person:{get_env('LINKEDIN_PROFILE_ID')}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post["body"]},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }
    r = requests.post(url, headers=headers, json=payload)
    return r.status_code == 201

def push_to_facebook(post):
    token = get_env("FACEBOOK_PAGE_ACCESS_TOKEN")
    page_id = get_env("FACEBOOK_PAGE_ID")
    url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {
        "message": post["body"],
        "access_token": token
    }
    r = requests.post(url, data=payload)
    return r.status_code == 200

def send_email(post):
    api_key = get_env("EMAIL_API_KEY")
    sender = get_env("EMAIL_SENDER_ADDRESS")
    url = "https://api.emailservice.com/send"
    payload = {
        "from": sender,
        "to": ["subscriber@list.com"],
        "subject": post["title"],
        "text": post["body"]
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.post(url, json=payload, headers=headers)
    return r.status_code == 202

def trigger_make_webhook():
    url = get_env("MAKE_WEBHOOK_URL")
    r = requests.post(url, json={"status": "syndication_complete"})
    return r.status_code == 200

def log_event(post, result):
    log_path = LOGS / f"syndication_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {post['title']} → {result}\n")

def main():
    posts = load_content()
    for post in posts:
        results = []
        if push_to_wordpress(post): results.append("WordPress ✅")
        if push_to_linkedin(post): results.append("LinkedIn ✅")
        if push_to_facebook(post): results.append("Facebook ✅")
        if send_email(post): results.append("Email ✅")
        log_event(post, ", ".join(results))
    trigger_make_webhook()
    print("✅ Syndication complete and logged.")

if __name__ == "__main__":
    main()