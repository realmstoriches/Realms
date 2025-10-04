import json, random, string
from datetime import datetime

VAULT = r"F:\Realms\envs\.env.vault"
ROTATION_LOG = r"F:\Realms\logs\credential_rotation.log"

def generate_secret(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def rotate():
    with open(VAULT, "r") as f:
        vault = json.load(f)
    for agent, creds in vault.items():
        for key in creds:
            old = creds[key]
            new = generate_secret()
            creds[key] = new
            log(f"{agent}.{key} rotated")
    with open(VAULT, "w") as f:
        json.dump(vault, f, indent=2)

def log(msg):
    with open(ROTATION_LOG, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")
    print(msg)

if __name__ == "__main__":
    rotate()