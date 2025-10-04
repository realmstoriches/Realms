# realms_dispatch_unified.py
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# === ENV HYGIENE ===
ENV_PATH = Path("F:/Realms/realms_core_alpha/.env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

# === PROXY POOL ===
def fetch_free_proxies():
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=US&ssl=all&anonymity=elite"
    try:
        r = requests.get(url, timeout=5)
        proxies = r.text.strip().split("\n")
        return [p.strip() for p in proxies if p.strip()]
    except Exception as e:
        print("❌ Proxy fetch failed:", e)
        return []

def validate_proxy(proxy_ip):
    proxy = {"http": f"http://{proxy_ip}", "https": f"http://{proxy_ip}"}
    try:
        r = requests.get("https://httpbin.org/ip", proxies=proxy, timeout=5)
        return r.status_code == 200
    except:
        return False

def get_valid_proxy():
    pool = fetch_free_proxies()
    for proxy_ip in pool:
        if validate_proxy(proxy_ip):
            print(f"✅ Proxy validated: {proxy_ip}")
            return {"http": f"http://{proxy_ip}", "https": f"http://{proxy_ip}"}
    print("❌ No valid proxies found.")
    return None

PROXIES = get_valid_proxy()

# === UNIFIED DISPATCH ===
def dispatch_to_platform(platform, payload, proxies=None):
    endpoints = {
        "wordpress": "https://your-wordpress-endpoint.com/api/post",
        "linkedin": "https://api.linkedin.com/v2/share",
        "email": "https://your-email-endpoint.com/send",
        "facebook": "https://graph.facebook.com/v12.0/me/feed"
    }
    url = endpoints.get(platform)
    if not url:
        print(f"❌ Unknown platform: {platform}")
        return
    try:
        r = requests.post(url, json=payload, proxies=proxies, timeout=10)
        print(f"✅ {platform.capitalize()} dispatch success: {r.status_code}")
    except Exception as e:
        print(f"❌ {platform.capitalize()} dispatch failed: {e}")

# === PAYLOADS ===
payloads = {
    "wordpress": {"title": "Hello World", "content": "This is a WordPress post."},
    "linkedin": {"text": "This is a LinkedIn update."},
    "email": {"to": "user@example.com", "subject": "Test Email", "body": "Hello from Realms."},
    "facebook": {"message": "This is a Facebook post."}
}

# === DISPATCH CYCLE ===
print("\n🚀 Unified Dispatch Cycle Initiated\n")
for platform, payload in payloads.items():
    dispatch_to_platform(platform, payload, proxies=PROXIES)
    time.sleep(1)

print("\n🔒 Unified dispatch complete. All platforms cycled.")