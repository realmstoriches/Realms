import os, requests, json

def dispatch_to_linkedin(payload):
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    author_urn = os.getenv("LINKEDIN_PROFILE_URN")  # e.g. "urn:li:person:abc123"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": f"{payload['title']}\n\n{payload['content']}\n\n{payload['cta']}"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        res = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=body)
        res.raise_for_status()
        print("✅ LinkedIn dispatch successful.")
        return res.json()
    except Exception as e:
        print(f"❌ LinkedIn dispatch failed: {e}")
        return None