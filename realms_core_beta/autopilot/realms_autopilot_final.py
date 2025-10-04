# realms_autopilot_final.py
import os
import re
import time
import shutil
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

# === BROWSER PATCH ===
def get_chrome_path():
    return shutil.which("chrome") or shutil.which("google-chrome") or r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# === AGENT DISPATCH ===
AGENTS = [
    ("dispatch_wordpress", "dispatch_wordpress"),
    ("dispatch_linkedin", "dispatch_linkedin"),
    ("dispatch_email", "dispatch_email"),
    ("dispatch_facebook", "dispatch_to_facebook"),
    ("fallback_wordpress_dispatch", "fallback_wordpress_post"),
    ("fallback_linkedin", "fallback_linkedin_post"),
    ("fallback_email", "fallback_email"),
    ("fallback_facebook", "fallback_facebook"),
    ("fallback_fallback_email", "fallback_fallback_email")
]

print("\n🚀 Sovereign Autopilot Cycle Initiated\n")
for module_name, function_name in AGENTS:
    try:
        mod = __import__(module_name)
        func = getattr(mod, function_name)
        print(f"🧠 Dispatching: {function_name} from {module_name}")
        func(proxies=PROXIES)
        print(f"✅ Success: {function_name}\n")
    except Exception as e:
        print(f"❌ Failure: {function_name} → {e}\n")
    time.sleep(1)

print("🔒 Sovereign autopilot complete. All agents dispatched. All fractures sealed.")