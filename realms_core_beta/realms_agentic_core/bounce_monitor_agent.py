import imaplib, email

def check_bounces(imap_server, imap_user, imap_pass):
    bounced = []
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(imap_user, imap_pass)
    mail.select("INBOX")
    typ, data = mail.search(None, '(FROM "MAILER-DAEMON")')
    for num in data[0].split():
        typ, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        bounced.append(msg.get("To"))
    mail.logout()
    return bounced

# Example usage
if __name__ == "__main__":
    bounces = check_bounces("imap.mailprovider.com", "founder@realms.ai", "your_app_password")
    print("🚫 Bounced Emails:", bounces)