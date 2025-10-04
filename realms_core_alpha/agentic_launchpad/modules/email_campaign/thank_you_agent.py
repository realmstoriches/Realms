from datetime import datetime

def send_thank_you_email(agent_name, crew_name, upsell_payload):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    subject = f"🙏 Thank You, {agent_name}"
    body = (
        f"Dear {agent_name},\n\n"
        f"Thank you for stepping in as a fallback agent for crew {crew_name}.\n"
        f"Your contribution ensured uninterrupted dispatch and operational sovereignty.\n\n"
        f"{upsell_payload['message']}\n\n"
        f"{upsell_payload['cta']}\n\n"
        f"Logged at {timestamp}"
    )

    print(f"📧 Sending thank-you email to {agent_name} in crew {crew_name}")
    print(f"📨 Subject: {subject}")
    print(f"📝 Body:\n{body}")