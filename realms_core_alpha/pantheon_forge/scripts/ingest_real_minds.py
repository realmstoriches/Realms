import json
import logging
import requests
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

json_path = os.path.join(os.path.dirname(__file__), "real_minds.json")
output_manifest = "expert_manifest.txt"
output_sources = "KNOWLEDGE_SOURCES.json"
output_log = "missing_fields_log.json"

# ✅ Load raw JSON
with open(json_path, "r", encoding="utf-8") as f:
    raw = "[" + f.read().strip().rstrip(",") + "]"

# ✅ Flatten nested lists
def flatten(data):
    flat = []
    def recurse(entry):
        if isinstance(entry, list):
            for item in entry:
                recurse(item)
        elif isinstance(entry, dict):
            flat.append(entry)
        else:
            logging.warning(f"⚠️ Skipping malformed item: {entry}")
    recurse(data)
    return flat

try:
    parsed = json.loads(raw)
    minds = flatten(parsed)
except Exception as e:
    logging.error(f"❌ Failed to parse or flatten real_minds.json: {e}")
    exit()

# ✅ Filter valid entries
valid_minds = []
invalid_minds = []
seen = set()

for mind in minds:
    if not all(k in mind for k in ["name", "domain", "contribution"]):
        invalid_minds.append(mind)
        continue
    name = mind["name"].strip().lower()
    if name not in seen:
        seen.add(name)
        valid_minds.append(mind)

logging.info(f"✅ {len(valid_minds)} unique valid minds")
logging.info(f"🗑️ {len(minds) - len(valid_minds)} duplicates removed")
logging.info(f"⚠️ {len(invalid_minds)} entries missing required fields")

# ✅ Write expert_manifest.txt
with open(output_manifest, "w", encoding="utf-8") as f:
    for mind in valid_minds:
        f.write(mind["name"] + "\n")
logging.info("✅ expert_manifest.txt written")

# ✅ Validate URLs
def validate_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

# ✅ Build KNOWLEDGE_SOURCES.json
sources_dict = {}
for mind in valid_minds:
    key = mind["name"].lower().replace(" ", "_")
    urls = mind.get("sources", [])
    valid_urls = [url for url in urls if validate_url(url)]
    sources_dict[key] = valid_urls
    logging.info(f"🔗 {mind['name']}: {len(valid_urls)} valid sources")

with open(output_sources, "w", encoding="utf-8") as f:
    json.dump(sources_dict, f, indent=4)
logging.info("✅ KNOWLEDGE_SOURCES.json built successfully")

# ✅ Log invalid entries
with open(output_log, "w", encoding="utf-8") as f:
    json.dump(invalid_minds, f, indent=4)
logging.info("🗂️ Invalid entries logged to missing_fields_log.json")