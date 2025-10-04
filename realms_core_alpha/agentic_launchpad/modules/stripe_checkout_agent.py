import requests
import json
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config_manager import get_env

LOGS = Path(__file__).resolve().parent.parent / "logs"
LOGS.mkdir(exist_ok=True)

def create_payment_link():
    key = get_env("STRIPE_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    product = {
        "name": "Realms Syndication Package",
        "description": "Automated outreach, monetization, and legacy creation",
        "amount": 4999,
        "currency": "usd"
    }

    # Create product
    prod_res = requests.post("https://api.stripe.com/v1/products", headers=headers, data={"name": product["name"]})
    prod_id = prod_res.json().get("id")

    # Create price
    price_res = requests.post("https://api.stripe.com/v1/prices", headers=headers, data={
        "unit_amount": product["amount"],
        "currency": product["currency"],
        "product": prod_id
    })
    price_id = price_res.json().get("id")

    # Create payment link
    link_res = requests.post("https://api.stripe.com/v1/payment_links", headers=headers, data={
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": 1
    })
    link = link_res.json().get("url")

    # Log it
    log_path = LOGS / "payment_links.json"
    if log_path.exists():
        with open(log_path) as f:
            data = json.load(f)
    else:
        data = []
    data.append({"timestamp": datetime.now().isoformat(), "url": link})
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"💳 Stripe Payment Link Created:\n{link}")

def inject_stripe_cta(content, stripe_url):
    return content + f"\n\n🔗 Activate here: {stripe_url}"

if __name__ == "__main__":
    create_payment_link()