import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def dispatch_email_campaign(recipients, content, image_url=None, video_url=None):
    sender = "your_email@domain.com"
    password = "your_email_password"

    for recipient in recipients:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Realms Dispatch Activation"
        msg["From"] = sender
        msg["To"] = recipient

        html = f"""
        <html>
            <body>
                <h2>Realms Dispatch</h2>
                <p>{content}</p>
                {'<img src="' + image_url + '" width="600"/>' if image_url else ''}
                {'<video width="600" controls><source src="' + video_url + '" type="video/mp4"></video>' if video_url else ''}
                <p><a href="https://www.realmstoriches.xyz">Visit Dashboard</a></p>
            </body>
        </html>
        """

        msg.attach(MIMEText(html, "html"))

        try:
            server = smtplib.SMTP("smtp.yourprovider.com", 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
            server.quit()
            print(f"✅ Email sent to {recipient}")
        except Exception as e:
            print(f"❌ Email failed for {recipient}: {e}")

