# realms_autopilot_patch.py
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

# === PATCH AGENTS ===
AGENT_PATH = Path("F:/Realms/realms_core_alpha")
AGENT_MODULES = [
    "dispatch_wordpress.py",
    "dispatch_linkedin.py",
    "dispatch_email.py",
    "dispatch_facebook.py",
    "fallback_wordpress_dispatch.py",
    "fallback_linkedin.py",
    "fallback_email.py",
    "fallback_facebook.py",
    "fallback_fallback_email.py"
]

def patch_agent(file):
    path = AGENT_PATH / file
    if not path.exists():
        print(f"❌ Missing: {file}")
        return

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    patched = []
    found_def = False
    for line in lines:
        if re.match(r"def \\w+\\(", line):
            found_def = True
            if "proxies" not in line:
                line = re.sub(r"\\((.*?)\\)", r"(\\1, proxies=None)", line)
        if "from dispatch import" in line:
            line = line.replace("from dispatch import", "from dispatch_email import")
        patched.append(line)

    if found_def:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(patched)
        print(f"🔧 Patched: {file}")
    else:
        print(f"⚠️ No dispatch function found in: {file}")

print("\n🛠️ Sovereign Patch Cycle Initiated\n")
for module in AGENT_MODULES:
    patch_agent(module)
    time.sleep(0.5)

print("\n🔒 All agents patched. Ready for autopilot.")