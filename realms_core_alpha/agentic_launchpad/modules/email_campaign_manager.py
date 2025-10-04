import smtplib, json
from email.mime.text import MIMEText

def build_campaign():
    return "Welcome to Realms. Your sovereign system is now live."

def send_email():
    msg = MIMEText(build_campaign())
    msg["Subject"] = "Realms Monetization Launch"
    msg["From"] = "realms@sovereign.system"
    msg["To"] = "robert.demotto@yourdomain.com"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("robertdemottojr83@gmail.com", "vaew wkbt mjxu hciz")
        server.send_message(msg)
        print("📧 Email campaign sent and forwarded.")

if __name__ == "__main__":
    send_email()