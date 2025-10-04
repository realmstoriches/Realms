import os
import requests
from dotenv import load_dotenv

# === CONFIGURATION ===
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PROFILE_URN = os.getenv("LINKEDIN_PROFILE_URN")

if not ACCESS_TOKEN or not PROFILE_URN:
    raise Exception("❌ Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_PROFILE_URN in .env")

# === POST PAYLOAD ===
def create_linkedin_post(text, media=None):
    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202509"
    }

    payload = {
        "author": PROFILE_URN,
        "commentary": text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False
    }

    if media:
        payload["content"] = {
            "media": [media]
        }

    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        print("✅ LinkedIn post published successfully.")
        return res.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ LinkedIn post failed: {e.response.status_code} {e.response.text}")
    except Exception as e:
        print(f"❌ LinkedIn dispatch error: {e}")

# === EXAMPLE USAGE ===
if __name__ == "__main__":
    create_linkedin_post("🚀 Realms is now fully credentialed for LinkedIn dispatch via versioned Marketing API.")