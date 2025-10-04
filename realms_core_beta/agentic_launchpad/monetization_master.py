import requests, json
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).resolve().parent))
from config_manager import get_env

BASE = Path(__file__).resolve().parent
LOGS = BASE / "logs"
LOGS.mkdir(exist_ok=True)

def create_product():
    key = get_env("STRIPE_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    r = requests.post("https://api.stripe.com/v1/products", headers=headers, data={"name": "Realms Syndication Package"})
    return r.json().get("id") if r.status_code == 200 else None

def create_price(product_id):
    key = get_env("STRIPE_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    data = {"unit_amount": 4999, "currency": "usd", "product": product_id}
    r = requests.post("https://api.stripe.com/v1/prices", headers=headers, data=data)
    return r.json().get("id") if r.status_code == 200 else None

def create_payment_link(price_id):
    key = get_env("STRIPE_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    data = {"line_items[0][price]": price_id, "line_items[0][quantity]": 1}
    r = requests.post("https://api.stripe.com/v1/payment_links", headers=headers, data=data)
    return r.json().get("url") if r.status_code == 200 else None

def log_link(link):
    log_path = LOGS / "payment_links.json"
    data = json.load(open(log_path)) if log_path.exists() else []
    data.append({"timestamp": datetime.now().isoformat(), "url": link})
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💳 Stripe Payment Link Created:\n{link}")

def main():
    print("🧠 Running monetization master...")
    product_id = create_product()
    if not product_id: return print("❌ Product creation failed.")
    price_id = create_price(product_id)
    if not price_id: return print("❌ Price creation failed.")
    link = create_payment_link(price_id)
    if not link: return print("❌ Payment link creation failed.")
    log_link(link)
    print("✅ Monetization pipeline complete.")

if __name__ == "__main__":
    main()