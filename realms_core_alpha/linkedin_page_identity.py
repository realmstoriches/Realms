import os
import requests
from dotenv import load_dotenv

# === CONFIGURATION ===
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
VERSION_HEADER = "202509"

def patch_env(key, value):
    try:
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
    except Exception as e:
        print(f"❌ Failed to patch .env: {e}")

def fetch_page_urn():
    if not ACCESS_TOKEN:
        print("❌ Missing LINKEDIN_ACCESS_TOKEN in .env")
        return

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "LinkedIn-Version": VERSION_HEADER
    }

    url = "https://api.linkedin.com/rest/organizations?q=roleAssignee&role=ADMINISTRATOR"

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        data = res.json()

        if "elements" not in data or not data["elements"]:
            print("❌ No LinkedIn Pages found for this token.")
            return

        org = data["elements"][0]
        urn = org.get("organizationalTarget", None)

        if not urn:
            print("❌ Could not extract organization URN.")
            return

        print(f"🧠 LinkedIn Page URN: {urn}")
        patch_env("LINKEDIN_PAGE_URN", urn)
        patch_env("LINKEDIN_PROFILE_URN", urn)
        print("✅ Dispatch identity is now wired for Page publishing.")
    except Exception as e:
        print(f"❌ Failed to fetch LinkedIn Page URN: {e}")

if __name__ == "__main__":
    fetch_page_urn()