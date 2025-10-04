import os
from pathlib import Path
from datetime import datetime
import json

BASE = Path("F:/Realms/realms_core_alpha/agentic_launchpad")
ENV = BASE / ".env"
LOGS = BASE / "logs"
MODULES = BASE / "modules"
LOGS.mkdir(exist_ok=True)

def patch_env():
    if not ENV.exists():
        print(f"⚠️ .env file not found at {ENV}. Creating...")
        ENV.write_text("", encoding="utf-8")

    with open(ENV, "r") as f:
        lines = f.readlines()

    env = {}
    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            key, val = line.strip().split("=", 1)
            env[key.strip()] = val.strip().strip('"').strip("'")

    updates = {
        "AGENTIC_API_KEY": "agentic-local-dev-key",
        "LINKEDIN_ACCESS_TOKEN": "[insert-your-token]",
        "FACEBOOK_PAGE_ACCESS_TOKEN": "[insert-your-token]"
    }

    with open(ENV, "a") as f:
        for key, val in updates.items():
            if key not in env or env[key] in ("", "[empty]", "[insert-your-token]"):
                f.write(f"{key}={val}\n")
                print(f"🔧 Patched {key} → {val}")

def patch_stripe_gateway():
    path = MODULES / "stripe_gateway.py"
    if path.exists():
        code = path.read_text(encoding="utf-8")
        if "agentic_launchpad.config_manager" in code:
            patched = code.replace(
                "from agentic_launchpad.config_manager import get_env",
                "import sys\nfrom pathlib import Path\nsys.path.append(str(Path(__file__).resolve().parent.parent))\nfrom config_manager import get_env"
            )
            path.write_text(patched, encoding="utf-8")
            print("🔧 Patched stripe_gateway.py import path")

def drop_transaction_tracker():
    code = """import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LOGS = BASE / "logs"
LOGS.mkdir(exist_ok=True)

def log_transaction(amount, source, status):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "amount": amount,
        "source": source,
        "status": status
    }
    log_path = LOGS / "transactions.json"
    if log_path.exists():
        with open(log_path) as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(log_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💰 Logged transaction: ${amount} from {source} → {status}")

if __name__ == "__main__":
    log_transaction(49.99, "Stripe", "Success")
"""
    (MODULES / "transaction_tracker.py").write_text(code, encoding="utf-8")
    print("📈 Dropped transaction_tracker.py")

def vercel_guidance():
    print("\n🌐 Vercel Deployment Guidance:")
    print("- Connect your GitHub repo to Vercel")
    print("- Set your blog subdomain in Vercel: blog.realmstoriches.xyz")
    print("- Use your VERCEL_DEPLOY_HOOK to trigger builds from agents")
    print("- Agents can push content to WordPress or static markdown in repo")

def log_filler_actions():
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "actions": ["patch_env", "patch_stripe_gateway", "drop_transaction_tracker", "vercel_guidance"]
    }
    with open(LOGS / "filler.json", "w") as f:
        json.dump(log_entry, f, indent=2)
def inject_website_link(content, website_url):
    return content + f"\n\n🌐 Visit us: {website_url}"

def main():
    print("🧠 Running final filler...")
    patch_env()
    patch_stripe_gateway()
    drop_transaction_tracker()
    vercel_guidance()
    log_filler_actions()
    print("✅ Final filler complete. You're ready to go live.")

if __name__ == "__main__":
    main()