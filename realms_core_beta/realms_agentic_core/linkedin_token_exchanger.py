import requests
import os
from dotenv import load_dotenv

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"  # Must match your LinkedIn app
AUTH_CODE = "AQSKQy2HwkDUXfpW80D6AxH2Cgr5qFeRXLaZm96EvtauiShq9BEwT7Bsu3XqKcOy4s-9XI7hfkj8IOhU-RGn3-7jZv66zEWRt3L6KOLsQICaEwtoOw2C6RcAl6nj-RiN6du_dnV1F_XklVFmNC1f_He7PAgOqqf_3-95CifAL-u0r5dZ2_E2a5PXLWPXgVJFg22VCq4sohPMGFb2xyk"

def patch_env(key, value):
    lines = []
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
    if not found:
        lines.append(f"{key}={value}\n")
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"✅ .env patched: {key}")

def exchange_code_for_token():
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": AUTH_CODE,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = requests.post(url, data=payload, headers=headers)
    res.raise_for_status()
    token = res.json()["access_token"]
    print(f"🔑 New LinkedIn Access Token: {token}")
    patch_env("LINKEDIN_ACCESS_TOKEN", token)

if __name__ == "__main__":
    exchange_code_for_token()