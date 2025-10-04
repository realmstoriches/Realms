import smtplib, os
from dotenv import load_dotenv

load_dotenv()

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_user = os.getenv("SMTP_USER")
smtp_pass = os.getenv("SMTP_PASS")

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_user, smtp_pass)
    print("✅ SMTP login successful — dispatch agent is ready.")
    server.quit()
except Exception as e:
    print("❌ SMTP login failed:", e)