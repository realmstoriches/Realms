import smtplib, os
from email.mime.text import MIMEText

def emergency_email(subject, message):
    sender = os.getenv("SMTP_EMAIL")
    password = os.getenv("SMTP_PASS")
    recipient = sender

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print("✅ Emergency email sent.")
    except Exception as e:
        print(f"❌ Emergency email failed: {e}")