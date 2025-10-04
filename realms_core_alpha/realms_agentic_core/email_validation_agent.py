import dns.resolver, smtplib

def validate_email_list(emails):
    return [email for email in emails if validate_email(email)]


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

if __name__ == "__main__":
    input_file = "harvested_emails.txt"
    output_file = "validated_emails.txt"

    try:
        with open(input_file) as f:
            raw_emails = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        exit()

    valid_emails = []
    for email in raw_emails:
        print(f"🔍 Validating: {email}")
        if validate_email(email):
            print(f"✅ Valid: {email}")
            valid_emails.append(email)
        else:
            print(f"❌ Invalid: {email}")

    with open(output_file, "w") as f:
        for email in valid_emails:
            f.write(email + "\n")

    print(f"\n✅ Validation complete — {len(valid_emails)} valid emails saved to {output_file}")