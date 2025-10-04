import requests
from .dispatch_variant_agent import generate_variant

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/e3afcnngjoil9igmy86bxdy1oms6pne8"

def trigger_make_scenario(content):
    variant = generate_variant(payment_link="https://realms.ai/pay")
    enriched = content + "\n\n" + variant["content"]

    payload = {
        "title": variant["title"],
        "content": variant["content"],
        "linkedin_urn": "urn:li:organization:108123328",
        "facebook_page_id": "875761185609852",
        "wordpress_site_url": "https://robertdemottojr83-tgljh.wordpress.com",
        "wordpress_username": "robertdemottojr83",
        "wordpress_password": "r2kkzl4t3naphbx4"
    }

    try:
        res = requests.post(MAKE_WEBHOOK_URL, json=payload)
        res.raise_for_status()
        print(f"📡 Dispatch Triggered: {res.status_code}")
    except Exception as e:
        print(f"❌ Dispatch Failed: {e}")

    return enriched