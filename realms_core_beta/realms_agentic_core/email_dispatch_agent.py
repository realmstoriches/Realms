import smtplib
from email.mime.text import MIMEText
from dispatch_variant_agent_v6 import generate_variant

def send_email(recipient, sender_email, smtp_server, smtp_port, smtp_user, smtp_pass, payment_link=None):
    variant = generate_variant(payment_link)
    msg = MIMEText(variant["content"])
    msg["Subject"] = variant["title"]
    msg["From"] = sender_email
    msg["To"] = recipient

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, recipient, msg.as_string())

# Example usage
if __name__ == "__main__":
    send_email(
        recipient="contact@example.com",
        sender_email="founder@realms.ai",
        smtp_server="smtp.mailprovider.com",
        smtp_port=465,
        smtp_user="founder@realms.ai",
        smtp_pass="your_app_password",
        payment_link="https://realms.ai/pay"
    )