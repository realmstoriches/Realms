import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

# ✅ Load .env from sovereign path
ENV_PATH = Path("F:/Realms/realms_core_alpha/.env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

# ✅ Scan realms_autopilot.py for rogue load_dotenv and commented dispatch/fallback lines
TARGET_FILE = "realms_autopilot.py"
with open(TARGET_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

rogue_dotenv = [i for i, line in enumerate(lines) if "load_dotenv()" in line and "ENV_PATH" not in line]
commented_lines = [line.strip() for line in lines if line.strip().startswith("#")]

print("\n🔍 Rogue load_dotenv() calls:")
for i in rogue_dotenv:
    print(f"Line {i+1}: {lines[i].strip()}")

print("\n🧩 Commented lines (dispatch/fallback candidates):")
for line in commented_lines:
    if "dispatch" in line.lower() or "fallback" in line.lower():
        print(line)

# ✅ Proxy validation
PROXIES = {
    "http": "http://username:password@proxy_ip:proxy_port",
    "https": "http://username:password@proxy_ip:proxy_port"
}

def validate_proxy():
    try:
        r = requests.get("https://httpbin.org/ip", proxies=PROXIES, timeout=5)
        print("\n🌐 Proxy IP:", r.json())
    except Exception as e:
        print("\n❌ Proxy validation failed:", e)

validate_proxy()