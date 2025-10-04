import os
from dotenv import load_dotenv

# === CONFIGURATION ===
ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(dotenv_path=ENV_PATH, override=True)

ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
PROFILE_URN = os.getenv("LINKEDIN_PROFILE_URN")
PAGE_URN = os.getenv("LINKEDIN_PAGE_URN")

def patch_env(key, value):
    try:
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
    except Exception as e:
        print(f"❌ Failed to patch .env: {e}")

def validate_env():
    print("🔍 Validating LinkedIn dispatch credentials...\n")

    if not ACCESS_TOKEN:
        print("❌ Missing LINKEDIN_ACCESS_TOKEN")
        return

    if PROFILE_URN:
        print(f"✅ Active URN: {PROFILE_URN} (personal)")
        return

    if PAGE_URN:
        print(f"⚠️ Missing LINKEDIN_PROFILE_URN, but PAGE_URN is available.")
        print(f"🔁 Using fallback URN: {PAGE_URN}")
        patch_env("LINKEDIN_PROFILE_URN", PAGE_URN)
        return

    print("❌ No valid URN found. Add LINKEDIN_PROFILE_URN or LINKEDIN_PAGE_URN to .env")

if __name__ == "__main__":
    validate_env()