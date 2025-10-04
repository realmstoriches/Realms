import os
import time
import hashlib
import psutil
import shutil
from pathlib import Path
from datetime import datetime

ENV_PATH = Path("F:/Realms/realms_core_alpha/.env")
BACKUP_PATH = ENV_PATH.with_suffix(".env.bak")
LOG_PATH = Path("F:/Realms/realms_core_alpha/env_guardian.log")

def safe_read(path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return None

def safe_write(path, content):
    try:
        path.write_text(content, encoding="utf-8")
    except Exception as e:
        print(f"❌ Failed to write {path.name}: {e}")

def heal_env():
    lines = safe_read(ENV_PATH).splitlines()
    clean = []
    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            key, val = line.strip().split("=", 1)
            val = val.strip()
            if any(c in val for c in ['#', '*', ' ', '(', ')']):
                val = '"' + val.strip().strip('"').strip("'") + '"'
            clean.append(f"{key.strip()}={val}\n")
        else:
            clean.append(line + "\n")
    safe_write(ENV_PATH, "".join(clean))
    print("✅ .env healed")

def lock_env():
    os.chmod(ENV_PATH, 0o444)  # Read-only
    print("🔒 .env locked")

def unlock_env():
    os.chmod(ENV_PATH, 0o644)  # Writable
    print("🔓 .env unlocked")

def hash_file(path):
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception:
        return None

def log_change(message):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def find_accessing_processes():
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            for file in proc.info['open_files'] or []:
                if file.path == str(ENV_PATH):
                    log_change(f"🔍 Accessed by PID {proc.info['pid']} → {proc.info['name']}")
        except Exception:
            continue

def restore_if_changed():
    current = hash_file(ENV_PATH)
    original = hash_file(BACKUP_PATH)
    if current != original:
        log_change( ".env tampered! Restoring backup...")
        unlock_env()
        shutil.copy(BACKUP_PATH, ENV_PATH)
        lock_env()
        log_change("✅ .env restored and re-locked.")

def monitor_env(interval=5):
    print("🛡️ Monitoring .env for changes...")
    last_hash = hash_file(ENV_PATH)
    while True:
        time.sleep(interval)
        current_hash = hash_file(ENV_PATH)
        if current_hash != last_hash:
            log_change(" .env file changed!")
            find_accessing_processes()
            restore_if_changed()
            last_hash = current_hash

def run_guardian():
    heal_env()
    shutil.copy(ENV_PATH, BACKUP_PATH)
    lock_env()
    monitor_env()

if __name__ == "__main__":
    run_guardian()