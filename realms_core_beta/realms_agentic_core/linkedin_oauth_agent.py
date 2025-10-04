import os
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"
PORT = 8080

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

def exchange_code_for_token(code):
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
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
    print(f"🔑 LinkedIn Access Token: {token}")
    patch_env("LINKEDIN_ACCESS_TOKEN", token)

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if "code" in query:
            code = query["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b" Authorization successful. You may close this window.")
            exchange_code_for_token(code)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b" Authorization failed.")

def start_server():
    server = HTTPServer(("localhost", PORT), OAuthHandler)
    print(f"🌐 Waiting for LinkedIn redirect on port {PORT}...")
    server.handle_request()

def initiate_oauth():
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=w_member_social"
    )
    print(f"🌐 Opening browser for LinkedIn authorization...")
    webbrowser.open(auth_url)
    start_server()

if __name__ == "__main__":
    initiate_oauth()