import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parent
LOGS = BASE / "logs"
heatmap_path = LOGS / "traffic_heatmap.json"

def build_heatmap():
    print("\n📈 Building Traffic Heatmap...")
    platforms = ["LinkedIn", "Twitter", "Facebook"]
    heatmap = {p: {"clicks": 0, "engagement": 0} for p in platforms}

    # Simulated click log
    click_log = LOGS / "click_log.json"
    if click_log.exists():
        with open(click_log) as f:
            clicks = json.load(f)
        for entry in clicks:
            platform = entry.get("platform")
            if platform in heatmap:
                heatmap[platform]["clicks"] += 1
                heatmap[platform]["engagement"] += entry.get("engagement", 1)

    with open(heatmap_path, "w") as f:
        json.dump(heatmap, f, indent=2)

    print("✅ Traffic heatmap saved to traffic_heatmap.json")
    print(json.dumps(heatmap, indent=2))

if __name__ == "__main__":
    build_heatmap()