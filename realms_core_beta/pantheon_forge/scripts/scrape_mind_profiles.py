import json
import logging
import requests
from bs4 import BeautifulSoup
import os
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

input_file = "validated_urls.json"
output_file = "mind_profiles.json"
error_log = "scrape_failures.json"

# ✅ Load URLs
with open(input_file, "r", encoding="utf-8") as f:
    url_map = json.load(f)

profiles = []
failures = {}

# ✅ Clean text
def clean(text):
    return re.sub(r"\s+", " ", text).strip()

# ✅ Extract quotes
def extract_quotes(text):
    return re.findall(r'“([^”]+)”', text) + re.findall(r'"([^"]+)"', text)

# ✅ Scrape logic
def scrape(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        return clean(text)
    except Exception as e:
        return None

# ✅ Process each mind
for key, urls in url_map.items():
    for url in urls:
        content = scrape(url)
        if content:
            quotes = extract_quotes(content)
            role_keywords = [kw for kw in ["management", "leadership", "innovation", "design", "strategy", "culture", "systems"] if kw in content.lower()]
            profiles.append({
                "name": key.replace("_", " ").title(),
                "source": url,
                "bio": content[:2000],
                "quotes": quotes[:5],
                "role_context": role_keywords
            })
            logging.info(f"🧠 {key}: scraped from {url}")
            break
    else:
        failures[key] = urls
        logging.warning(f"❌ {key}: all URLs failed")

# ✅ Write outputs
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(profiles, f, indent=4)

with open(error_log, "w", encoding="utf-8") as f:
    json.dump(failures, f, indent=4)

logging.info(f"✅ mind_profiles.json written")
logging.info(f"🗂️ Failures logged to scrape_failures.json")