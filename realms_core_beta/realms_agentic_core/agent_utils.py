# agent_utils.py
import dns.resolver, smtplib

def validate_email(email):
    domain = email.split('@')[-1]
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_host = str(mx_records[0].exchange)
        server = smtplib.SMTP()
        server.connect(mx_host)
        server.helo()
        server.mail('test@realms.ai')
        code, _ = server.rcpt(email)
        server.quit()
        return code == 250
    except Exception:
        return False