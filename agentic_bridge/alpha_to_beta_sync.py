import os
import shutil
import logging
import datetime

# === CONFIGURATION ===
ALPHA_PATH = r"F:\Realms\realms_core_alpha"
BETA_PATH = r"F:\Realms\realms_core_beta"
LOG_PATH = r"F:\sync_logs\alpha_to_beta.log"
EXCLUDE = {'.git', '__pycache__', 'node_modules', '.env', '.env.*', '*.txt'}

# === SETUP LOGGING ===
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s - %(message)s')

def log(msg):
    print(msg)
    logging.info(msg)

def should_exclude(name):
    for pattern in EXCLUDE:
        if pattern.startswith('*') and name.endswith(pattern[1:]):
            return True
        if pattern.endswith('*') and name.startswith(pattern[:-1]):
            return True
        if name == pattern:
            return True
    return False

def sync_folder(src, dst):
    for root, dirs, files in os.walk(src):
        rel_path = os.path.relpath(root, src)
        target_dir = os.path.join(dst, rel_path)
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            if should_exclude(file):
                continue
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            shutil.copy2(src_file, dst_file)
            log(f"✅ Synced: {dst_file}")

def run_sync():
    log("🚀 Starting sync from realms_core_alpha to realms_core_beta...")
    sync_folder(ALPHA_PATH, BETA_PATH)
    log("🎯 Sync complete.")

if __name__ == "__main__":
    run_sync()