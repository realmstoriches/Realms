import json
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
