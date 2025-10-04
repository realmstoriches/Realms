from dispatch.dispatch_facebook import dispatch_to_facebook
import json

def retry_facebook():
    try:
        with open("logs/last_payload.json", "r") as f:
            payload = json.load(f)
        result = dispatch_to_facebook(payload)
        if result:
            print("🛠️ Facebook fallback succeeded.")
        else:
            print("❌ Facebook fallback failed.")
    except Exception as e:
        print(f"❌ Error loading fallback payload: {e}")