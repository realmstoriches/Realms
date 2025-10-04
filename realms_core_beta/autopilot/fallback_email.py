import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dispatch_email import dispatch_email
import json


def retry_email():
    try:
        with open("logs/last_payload.json", "r") as f:
            payload = json.load(f)
        dispatch_email(payload)
    except Exception as e:
        print(f"❌ Email fallback failed: {e}")