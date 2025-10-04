import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config_manager import get_env

def activate_gateway():
    key = get_env("STRIPE_API_KEY")
    if not key or key == "[empty]":
        print("⚠️ Stripe API key missing. Monetization paused.")
    else:
        print(f"✅ Stripe gateway activated with key: {key[:6]}...")

if __name__ == "__main__":
    activate_gateway()
