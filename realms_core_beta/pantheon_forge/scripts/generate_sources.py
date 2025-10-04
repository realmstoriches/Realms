import urllib.parse
import requests
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ HEAD request validator
def validate_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except Exception as e:
        logging.warning(f"HEAD request failed for {url}: {e}")
        return False

# ✅ Generate high-quality sources
def generate_sources(name):
    encoded = urllib.parse.quote(name)
    urls = [
        f"https://en.wikipedia.org/wiki/{encoded}",
        f"https://www.ted.com/search?q={encoded}",
        f"https://www.semanticscholar.org/search?q={encoded}",
        f"https://www.youtube.com/results?search_query={encoded}+interview",
        f"https://github.com/search?q={encoded}",
        f"https://medium.com/search?q={encoded}",
        f"https://{name.lower().replace(' ', '')}.com"
    ]
    return [url for url in urls if validate_url(url)]

# ✅ Fallback logic
def fallback_sources(name):
    encoded = urllib.parse.quote(name)
    return [
        f"https://en.wikipedia.org/wiki/{encoded}",
        f"https://www.goodreads.com/search?q={encoded}"
    ]

# ✅ Main runner
if __name__ == "__main__":
    with open("expert_manifest.txt", "r", encoding="utf-8") as f:
        expert_list = [line.strip() for line in f.readlines()]

    knowledge_sources = {}
    for name in expert_list:
        logging.info(f"🔍 Generating sources for: {name}")
        sources = generate_sources(name)
        if not sources:
            logging.warning(f"⚠️ No valid sources found for {name}. Using fallback.")
            sources = fallback_sources(name)
        knowledge_sources[name.lower().replace(" ", "_")] = sources

    with open("KNOWLEDGE_SOURCES.json", "w", encoding="utf-8") as f:
        json.dump(knowledge_sources, f, indent=4)

    logging.info("✅ Knowledge sources saved to KNOWLEDGE_SOURCES.json")