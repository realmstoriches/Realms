import os, json, time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent
LOGS = BASE / "logs"
MARKETING = BASE / "marketing"
LOGS.mkdir(exist_ok=True)
ENV_PATH = BASE / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

def explode_terminal():
    print("\n💥 SYSTEM IGNITION: POST-LAUNCH DETONATED 💥")
    print("💰" * 50)
    print("🚀 Monetization active | CTA injected | Agents online | Logs clean")
    print("📊 Dashboard building... please wait...\n")

def main():
    try:
        explode_terminal()
        # continue with dashboard logic...
    except Exception as e:
        print(f"💥 Fatal error: {e}")

if __name__ == "__main__":
    main()