import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

PORT = 5050  # You can change this if needed

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

class TokenHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
            print(f"📨 Incoming token payload: {data}")

            # Example expected payload from Make:
            # {
            #   "platform": "linkedin",
            #   "access_token": "AQX..."
            # }

            platform = data.get("platform")
            token = data.get("access_token")

            if platform == "linkedin":
                patch_env("LINKEDIN_ACCESS_TOKEN", token)
            elif platform == "facebook":
                patch_env("FACEBOOK_ACCESS_TOKEN", token)
            elif platform == "wordpress":
                patch_env("WORDPRESS_PASSWORD", token)
            else:
                print("⚠️ Unknown platform in payload")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b" Token received and patched")
        except Exception as e:
            print(f"❌ Error processing token: {e}")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid payload")

def start_server():
    server = HTTPServer(("0.0.0.0", PORT), TokenHandler)
    print(f"🌐 Token listener active on port {PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    start_server()