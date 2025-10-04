import os
import re
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

# === TARGET FILE ===
TARGET = "realms_autopilot.py"
with open(TARGET, "r", encoding="utf-8") as f:
    lines = f.readlines()

# === FIND COMMENTED IMPORTS ===
commented_imports = []
for i, line in enumerate(lines):
    if line.strip().startswith("#from") and ("dispatch" in line or "fallback" in line):
        commented_imports.append((i, line.strip()))

# === TEST EACH IMPORT ===
print("\n🔍 Starting import validation cycle...\n")
for idx, line in commented_imports:
    print(f"🧪 Testing: {line}")
    # Uncomment line
    lines[idx] = line.replace("#", "", 1) + "\n"
    with open(TARGET, "w", encoding="utf-8") as f:
        f.writelines(lines)

    # Run test
    try:
        exec(open(TARGET).read(), {"PROXIES": PROXIES})
        print(f"✅ Passed: {line}")
    except Exception as e:
        print(f"❌ Failed: {line}\n   → {e}")
        # Re-comment line
        lines[idx] = "#" + line + "\n"
        with open(TARGET, "w", encoding="utf-8") as f:
            f.writelines(lines)

    time.sleep(1)

print("\n🔒 Cycle complete. Fractures logged. Sovereignty restored.")