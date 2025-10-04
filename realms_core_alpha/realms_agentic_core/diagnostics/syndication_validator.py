import json
import requests
from fallback.fallback_wordpress_dispatch import fallback_wordpress_post
from fallback.fallback_linkedin import fallback_linkedin_post

def validate_payload(payload):
    required_fields = ["title", "content"]
    return all(field in payload and payload[field] for field in required_fields)

def send_to_make(payload, url):
    try:
        response = requests.post(url, json=payload)
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)

def reroute_to_fallback(payload, platform):
    title = payload.get("title", "Untitled")
    content = payload.get("content", "No content provided")
    if platform == "wordpress":
        fallback_wordpress_post(title, content)
    elif platform == "linkedin":
        fallback_linkedin_post(title, content)

def dispatch(payload, platform, make_url):
    if validate_payload(payload):
        status, response = send_to_make(payload, make_url)
        print(f"✅ Make.com dispatch status: {status}")
        if status != 200:
            reroute_to_fallback(payload, platform)
    else:
        print("❌ Invalid payload. Rerouting...")
        reroute_to_fallback(payload, platform)

if __name__ == "__main__":
    test_payload = {"title": "Test", "content": "Hello World"}
    dispatch(test_payload, "wordpress", "https://hook.make.com/your-wordpress-id")

