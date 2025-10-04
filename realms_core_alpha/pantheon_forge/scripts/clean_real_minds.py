import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

json_path = os.path.join(os.path.dirname(__file__), "real_minds.json")
output_path = os.path.join(os.path.dirname(__file__), "real_minds_cleaned.json")

# ✅ Load raw file
with open(json_path, "r", encoding="utf-8") as f:
    raw = f.read()

# ✅ Wrap in brackets if needed
raw = "[" + raw.strip().rstrip(",") + "]"

try:
    data = json.loads(raw)
except Exception as e:
    logging.error(f"❌ Failed to parse real_minds.json: {e}")
    exit()

# ✅ Flatten nested lists
flat = []
def flatten(entry):
    if isinstance(entry, list):
        for item in entry:
            flatten(item)
    elif isinstance(entry, dict):
        flat.append(entry)
    else:
        logging.warning(f"⚠️ Skipping malformed item: {entry}")

flatten(data)

# ✅ Deduplicate by name
seen = set()
cleaned = []
for mind in flat:
    name = mind.get("name", "").strip().lower()
    if name and name not in seen:
        seen.add(name)
        cleaned.append(mind)

logging.info(f"✅ Cleaned {len(cleaned)} minds, removed {len(flat) - len(cleaned)} duplicates")

# ✅ Write cleaned file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=4)

logging.info(f"✅ Output saved to {output_path}")