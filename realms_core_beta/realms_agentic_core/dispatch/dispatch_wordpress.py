import os, requests, json

def dispatch_to_wordpress(payload):
    wp_url = os.getenv("WORDPRESS_SITE_URL") + "/wp-json/wp/v2/posts"
    headers = {
        "Authorization": f"Bearer {os.getenv('WP_TOKEN')}",
        "Content-Type": "application/json"
    }
    body = {
        "title": payload["title"],
        "content": f"{payload['content']}<br><br>{payload['cta']}",
        "status": "publish"
    }
    try:
        res = requests.post(wp_url, headers=headers, json=body, timeout=10)
        res.raise_for_status()
        print("✅ WordPress dispatch successful.")
        return res.json()
    except Exception as e:
        print(f"❌ WordPress dispatch failed: {e}")
        return None