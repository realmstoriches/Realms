import os, requests

def dispatch_email(payload):
    api_key = os.getenv("EMAIL_API_KEY")
    sender = os.getenv("EMAIL_SENDER_ADDRESS")
    recipient = os.getenv("EMAIL_SENDER_ADDRESS")  # Self-notification

    subject = f"Dispatch: {payload['title']}"
    body = f"{payload['content']}\n\n{payload['cta']}\n\nMedia:\n" + "\n".join(payload["media"])

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    email_payload = {
        "from": {"email": sender},
        "personalizations": [{
            "to": [{"email": recipient}],
            "subject": subject
        }],
        "content": [{
            "type": "text/plain",
            "value": body
        }]
    }

    try:
        res = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=email_payload)
        if res.status_code == 202:
            print("✅ Email dispatch successful.")
        else:
            print(f"❌ Email dispatch failed: {res.status_code} {res.text}")
    except Exception as e:
        print(f"❌ Email dispatch error: {e}")