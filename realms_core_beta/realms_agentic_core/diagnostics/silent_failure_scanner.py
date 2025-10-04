# silent_failure_scanner.py
import requests, json, smtplib
from datetime import datetime

MAKE_WEBHOOK_URL = "https://hook.make.com/your-scenario-id"
LOG_FILE = "failure_log.txt"
EMAIL_ALERT = "your@email.com"

def test_make_scenario(payload):
    try:
        response = requests.post(MAKE_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            log_failure(response.text)
            send_alert(response.text)
    except Exception as e:
        log_failure(str(e))
        send_alert(str(e))

def log_failure(error):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - ERROR: {error}\n")

def send_alert(error):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("your@email.com", "your-password")
    message = f"Subject: Make.com Failure\n\n{error}"
    server.sendmail("your@email.com", EMAIL_ALERT, message)
    server.quit()

# Example payload test
test_make_scenario({"test": "ping"})

