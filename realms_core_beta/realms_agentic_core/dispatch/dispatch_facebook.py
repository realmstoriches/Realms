import os
import requests
import json

def dispatch_to_facebook(payload):
    access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")

    post_url = f"https://graph.facebook.com/{page_id}/feed"
    message = f"{payload['title']}\n\n{payload['content']}\n\n{payload['cta']}"

    params = {
        "message": message,
        "access_token": access_token
    }

    try:
        res = requests.post(post_url, data=params, timeout=10)
        res.raise_for_status()
        print("✅ Facebook dispatch successful.")
        return res.json()
    except Exception as e:
        print(f"❌ Facebook dispatch failed: {e}")
        return None