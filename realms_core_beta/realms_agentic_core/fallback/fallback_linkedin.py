from dispatch.dispatch_linkedin import dispatch_to_linkedin
import json

def retry_linkedin():
    try:
        with open("logs/last_payload.json", "r") as f:
            payload = json.load(f)
        result = dispatch_to_linkedin(payload)
        if result:
            print("🛠️ LinkedIn fallback succeeded.")
        else:
            print("❌ LinkedIn fallback failed.")
    except Exception as e:
        print(f"❌ Error loading fallback payload: {e}")