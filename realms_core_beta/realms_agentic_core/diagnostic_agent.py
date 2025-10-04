import os
import smtplib
import imaplib
from dotenv import load_dotenv

load_dotenv()

def check_env():
    keys = [
        "SMTP_SERVER", "SMTP_PORT", "SMTP_USER", "SMTP_PASS",
        "IMAP_SERVER", "IMAP_USER", "IMAP_PASS"
    ]
    print("🔍 Checking .env variables:")
    for key in keys:
        val = os.getenv(key)
        status = "✅" if val else "❌"
        print(f"{status} {key}: {val if val else 'Missing'}")

def check_smtp():
    try:
        server = smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT")))
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        print("✅ SMTP login successful — dispatch agent is ready.")
        server.quit()
    except Exception as e:
        print("❌ SMTP login failed:", e)

def check_imap():
    try:
        mail = imaplib.IMAP4_SSL(os.getenv("IMAP_SERVER"))
        mail.login(os.getenv("IMAP_USER"), os.getenv("IMAP_PASS"))
        mail.select("INBOX")
        print("✅ IMAP login successful — bounce monitor is ready.")
        mail.logout()
    except Exception as e:
        print("❌ IMAP login failed:", e)

if __name__ == "__main__":
    check_env()
    print("\n📡 Verifying SMTP:")
    check_smtp()
    print("\n📬 Verifying IMAP:")
    check_imap()