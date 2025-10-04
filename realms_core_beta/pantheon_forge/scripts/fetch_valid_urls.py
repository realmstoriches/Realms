import json
import logging
import requests
import os
from urllib.parse import quote

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

input_file = "real_minds.json"
output_file = "validated_urls.json"
fallback_log = "url_fallback_log.json"

# ✅ Load minds
with open(input_file, "r", encoding="utf-8") as f:
    minds = json.load(f)

# ✅ Search templates
templates = [
    "https://en.wikipedia.org/wiki/{}",
    "https://www.ted.com/search?q={}",
    "https://www.linkedin.com/search/results/all/?keywords={}",
    "https://github.com/search?q={}",
    "https://www.google.com/search?q={}"
]

# ✅ Validate URL
def is_valid(url):
    try:
        r = requests.head(url, timeout=5)
        return r.status_code == 200
    except Exception:
        return False

# ✅ Build URL list
results = {}
fallbacks = {}

for mind in minds:
    name = mind.get("name", "").strip()
    key = name.lower().replace(" ", "_")
    urls = []

    for template in templates:
        url = template.format(quote(name))
        if is_valid(url):
            urls.append(url)

    if urls:
        results[key] = urls
        logging.info(f"🔗 {name}: {len(urls)} valid URLs")
    else:
        fallback = f"https://en.wikipedia.org/wiki/{quote(name)}"
        results[key] = [fallback]
        fallbacks[key] = fallback
        logging.warning(f"⚠️ {name}: no valid URLs found, using fallback")

# ✅ Write outputs
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4)

with open(fallback_log, "w", encoding="utf-8") as f:
    json.dump(fallbacks, f, indent=4)

logging.info(f"✅ validated_urls.json written")
logging.info(f"🗂️ Fallbacks logged to url_fallback_log.json")