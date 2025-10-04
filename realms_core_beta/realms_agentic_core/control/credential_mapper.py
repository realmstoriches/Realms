from dotenv import load_dotenv
import os

load_dotenv()

def get_credential(service):
    creds = {
        "wordpress": os.getenv("WP_TOKEN"),
        "linkedin": os.getenv("LINKEDIN_TOKEN"),
        "email": {
            "user": os.getenv("SMTP_EMAIL"),
            "pass": os.getenv("SMTP_PASS")
        },
        "fallback": os.getenv("FALLBACK_EMAIL")
    }
    return creds.get(service)

if __name__ == "__main__":
    print(get_credential("wordpress"))