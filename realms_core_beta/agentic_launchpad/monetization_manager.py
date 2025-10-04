import requests
import json
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
    data = {"name": "Realms Syndication Package"}
    r = requests.post("https://api.stripe.com/v1/products", headers=headers, data=data)
    if r.status_code == 200:
        return r.json().get("id")
    return None

def create_price(product_id):
    key = get_env("STRIPE_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    data = {
        "unit_amount": 4999,
        "currency": "usd",
        "product": product_id
    }
    r = requests.post("https://api.stripe.com/v1/prices", headers=headers, data=data)
    if r.status_code == 200:
        return r.json().get("id")
    return None

def create_payment_link(price_id):
    key = get_env("STRIPE_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    data = {
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": 1
    }
    r = requests.post("https://api.stripe.com/v1/payment_links", headers=headers, data=data)
    if r.status_code == 200:
        return r.json().get("url")
    return None

def log_link(link):
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

def fallback():
    log_path = LOGS / f"stripe_error_{datetime.now().strftime('%Y%m%d_%H%M')}.log"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("❌ Stripe monetization failed. Check API key and credentials.\n")
    print("❌ Stripe setup failed. Logged for oversight.")

def main():
    print("🧠 Running monetization master...")
    product_id = create_product()
    if not product_id:
        fallback()
        return
    price_id = create_price(product_id)
    if not price_id:
        fallback()
        return
    link = create_payment_link(price_id)
    if not link:
        fallback()
        return
    log_link(link)
    print("✅ Monetization pipeline complete.")

if __name__ == "__main__":
    main()