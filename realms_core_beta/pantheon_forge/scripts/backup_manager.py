import os
import zipfile
import datetime
import logging

VAULT_DIR = "./pantheon_vault"
BACKUP_DIR = "./pantheon_backups"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Create backup directory if missing
os.makedirs(BACKUP_DIR, exist_ok=True)

# ✅ Zip vault contents
def zip_vault():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"vault_backup_{timestamp}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)

    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(VAULT_DIR):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, VAULT_DIR)
                zipf.write(full_path, arcname)
    logging.info(f"✅ Vault backed up to {backup_path}")

# ✅ Main runner
if __name__ == "__main__":
    zip_vault()