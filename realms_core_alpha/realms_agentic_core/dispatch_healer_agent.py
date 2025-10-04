import os
import requests
from dotenv import load_dotenv
from datetime import datetime

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

def patch_env(key, value):
    lines = []
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
    if not found:
        lines.append(f"{key}={value}\n")
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"✅ .env patched: {key}")

def validate_linkedin():
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    urn = os.getenv("LINKEDIN_PROFILE_URN")
    if not token or not urn:
        print("❌ LinkedIn missing token or URN")
        return False
    headers = {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": "202509"
    }
    try:
        res = requests.get("https://api.linkedin.com/rest/posts", headers=headers)
        if res.status_code == 401:
            print("🔁 LinkedIn token expired or unauthorized")
            return False
        if res.ok:
            print("✅ LinkedIn token valid")
            return True
        print(f"❌ LinkedIn validation failed: {res.status_code}")
        return False
    except Exception as e:
        print(f"❌ LinkedIn validation error: {e}")
        return False

def validate_facebook():
    token = os.getenv("FACEBOOK_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    if not token or not page_id:
        print("❌ Facebook missing token or Page ID")
        return False
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
    try:
        res = requests.post(url, data={"message": "Test"}, params={"access_token": token})
        if res.status_code == 403:
            print("🔁 Facebook token lacks permission or is expired")
            return False
        if res.ok:
            print("✅ Facebook token valid")
            return True
        print(f"❌ Facebook validation failed: {res.status_code}")
        return False
    except Exception as e:
        print(f"❌ Facebook validation error: {e}")
        return False

def validate_wordpress():
    site = os.getenv("WORDPRESS_SITE_URL")
    user = os.getenv("WORDPRESS_USERNAME")
    pw = os.getenv("WORDPRESS_APP_PASSWORD") or os.getenv("WORDPRESS_PASSWORD")
    if not site or not user or not pw:
        print("❌ WordPress missing credentials")
        return False
    url = f"{site.rstrip('/')}/wp-json/wp/v2/posts"
    try:
        res = requests.get(url, auth=(user, pw))
        if res.status_code == 404:
            print("🔁 WordPress endpoint malformed")
            return False
        if res.ok:
            print("✅ WordPress credentials valid")
            return True
        print(f"❌ WordPress validation failed: {res.status_code}")
        return False
    except Exception as e:
        print(f"❌ WordPress validation error: {e}")
        return False

def heal_dispatch_failures():
    print("🧠 Healing Dispatch Chain...\n")
    linkedin_ready = validate_linkedin()
    facebook_ready = validate_facebook()
    wordpress_ready = validate_wordpress()

    if linkedin_ready and facebook_ready and wordpress_ready:
        print("\n📡 All systems green. Re-attempting dispatch...\n")
        os.system("python dispatch_syndicate_agent.py")
    else:
        print("\n⚠️ Healing incomplete. Manual intervention required.")

if __name__ == "__main__":
    heal_dispatch_failures()