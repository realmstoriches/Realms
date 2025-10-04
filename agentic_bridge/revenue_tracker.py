import os, json
from datetime import datetime

LOG_DIR = r"F:\Realms\logs\monetization"
REPORT = r"F:\Realms\agentic_bridge\revenue_report.json"

def parse_logs():
    total = 0
    entries = []
    for file in os.listdir(LOG_DIR):
        path = os.path.join(LOG_DIR, file)
        try:
            with open(path, "r") as f:
                lines = f.readlines()
            for line in lines:
                if "$" in line:
                    amount = float(line.strip().replace("$", ""))
                    total += amount
                    entries.append({"file": file, "amount": amount})
        except Exception:
            continue
    return total, entries

def run():
    total, entries = parse_logs()
    report = {
        "timestamp": str(datetime.now()),
        "total_revenue": total,
        "entries": entries
    }
    with open(REPORT, "w") as f:
        json.dump(report, f, indent=2)
    print(f"💰 Total Revenue: ${total:.2f}")

if __name__ == "__main__":
    run()