from dispatch.dispatch_email import dispatch_email
import json

def retry_email():
    try:
        with open("logs/last_payload.json", "r") as f:
            payload = json.load(f)
        dispatch_email(payload)
    except Exception as e:
        print(f"❌ Email fallback failed: {e}")