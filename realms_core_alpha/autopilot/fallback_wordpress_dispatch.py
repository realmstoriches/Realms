from dispatch.dispatch_wordpress import dispatch_to_wordpress
import json

def retry_wordpress():
    try:
        with open("logs/last_payload.json", "r") as f:
            payload = json.load(f)
        result = dispatch_to_wordpress(payload)
        if result:
            print("🛠️ WordPress fallback succeeded.")
        else:
            print("❌ WordPress fallback failed.")
    except Exception as e:
        print(f"❌ Error loading fallback payload: {e}")