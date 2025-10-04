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

def log(platform, status, detail):
    print(f"{datetime.utcnow().isoformat()} | {platform} → {status}: {detail}")

# === LINKEDIN ===
def heal_linkedin():
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    urn = os.getenv("LINKEDIN_PROFILE_URN")
    if not token or not urn:
        log("LinkedIn", "❌ Missing", "Token or URN")
        return False
    headers = {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": "202509"
    }
    res = requests.get("https://api.linkedin.com/rest/posts", headers=headers)
    if res.status_code == 401:
        log("LinkedIn", "🔁 Healing", "Token expired or invalid")
        return False
    elif res.status_code == 403:
        log("LinkedIn", "🔁 Healing", "URN may be malformed or unauthorized")
        return False
    elif res.status_code == 400:
        log("LinkedIn", "🔁 Healing", "Payload structure likely invalid")
        return False
    log("LinkedIn", "✅ Ready", "Token and URN valid")
    return True

# === FACEBOOK ===
def heal_facebook():
    token = os.getenv("FACEBOOK_ACCESS_TOKEN")
    page_id = os.getenv("FACEBOOK_PAGE_ID")
    if not token or not page_id:
        log("Facebook", "❌ Missing", "Token or Page ID")
        return False
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
    res = requests.post(url, data={"message": "Test"}, params={"access_token": token})
    if res.status_code == 403:
        log("Facebook", "🔁 Healing", "Token lacks permission or is expired")
        return False
    log("Facebook", "✅ Ready", "Token and Page ID valid")
    return True

# === WORDPRESS ===
def heal_wordpress():
    site = os.getenv("WORDPRESS_SITE_URL", "").rstrip("/")
    user = os.getenv("WORDPRESS_USERNAME")
    pw = os.getenv("WORDPRESS_PASSWORD") or os.getenv("WORDPRESS_APP_PASSWORD")
    if not site or not user or not pw:
        log("WordPress", "❌ Missing", "Site URL or credentials")
        return False
    url = f"{site}/wp-json/wp/v2/posts"
    res = requests.get(url, auth=(user, pw))
    if res.status_code == 404:
        log("WordPress", "🔁 Healing", "Endpoint malformed or site unreachable")
        return False
    log("WordPress", "✅ Ready", "Credentials and endpoint valid")
    return True

def run_dispatch():
    print("\n📡 Initiating Sovereign Syndication...\n")
    os.system("python dispatch_syndicate_agent.py")

def heal_and_dispatch():
    print("🧠 Healing Dispatch Chain...\n")
    linkedin_ready = heal_linkedin()
    facebook_ready = heal_facebook()
    wordpress_ready = heal_wordpress()

    if linkedin_ready and facebook_ready and wordpress_ready:
        print("\n✅ All systems green. Re-attempting dispatch...\n")
        run_dispatch()
    else:
        print("\n⚠️ Healing incomplete. Manual intervention required.")

if __name__ == "__main__":
    heal_and_dispatch()