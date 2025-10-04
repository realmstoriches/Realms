import os
import json
from pathlib import Path

def get_env(var_name, default=None):
    return os.getenv(var_name, default)


def load_config():
    print("⚙️ [config_manager] Loading system configuration...")

    config_path = Path(__file__).resolve().parent.parent / "config" / "system_config.json"
    if not config_path.exists():
        print("⚠️ Config file not found. Using defaults.")
        return {}

    try:
        config = json.loads(config_path.read_text())
        print(f"✅ Config loaded: {list(config.keys())}")
        return config
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return {}