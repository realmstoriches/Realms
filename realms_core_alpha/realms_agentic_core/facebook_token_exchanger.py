import os
import requests
from dotenv import load_dotenv

# === CONFIGURATION ===
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

USER_TOKEN = os.getenv("FACEBOOK_USER_ACCESS_TOKEN")
PAGE_ID = "875761185609852"
GRAPH_API_VERSION = "v18.0"

def get_page_token(user_token, page_id):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me/accounts"
    params = {"access_token": user_token}
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json().get("data", [])
        for page in data:
            if page.get("id") == page_id:
                token = page.get("access_token")
                print(f"🔐 Page Access Token: {token}")
                return token
        raise Exception(f"Page ID {page_id} not found in account list.")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code} {e.response.text}")
        raise
    except Exception as e:
        print(f"❌ Failed to retrieve page token: {e}")
        raise

def patch_env(token):
    try:
        lines = []
        if os.path.exists(ENV_PATH):
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()

        def upsert(key, value):
            found = False
            for i, line in enumerate(lines):
                if line.strip().startswith(f"{key}="):
                    lines[i] = f"{key}={value}\n"
                    found = True
            if not found:
                lines.append(f"{key}={value}\n")

        upsert("FACEBOOK_ACCESS_TOKEN", token)
        upsert("FACEBOOK_PAGE_ID", PAGE_ID)

        with open(ENV_PATH, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"✅ .env updated with Facebook Page token.")
    except Exception as e:
        print(f"❌ Failed to patch .env: {e}")
        raise

# === MAIN EXECUTION ===
if __name__ == "__main__":
    if not USER_TOKEN:
        print(f"❌ Missing FACEBOOK_USER_ACCESS_TOKEN in {ENV_PATH}")
        print("🔧 Please add it like this:\nFACEBOOK_USER_ACCESS_TOKEN=your_user_token_here")
        exit(1)

    try:
        page_token = get_page_token(USER_TOKEN, PAGE_ID)
        patch_env(page_token)
    except Exception as e:
        print(f"❌ Script failed: {e}")