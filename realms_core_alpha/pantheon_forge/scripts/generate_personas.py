import json
import logging
import os
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

profiles_file = "mind_profiles.json"
raw_file = "real_minds.json"
output_file = "persona_descriptions.json"

# ✅ Load scraped profiles
with open(profiles_file, "r", encoding="utf-8") as f:
    scraped = json.load(f)

# ✅ Load raw minds
with open(raw_file, "r", encoding="utf-8") as f:
    raw = json.load(f)

# ✅ Index raw minds
raw_index = {m["name"].strip().lower(): m for m in raw if "name" in m}

# ✅ Style presets
styles = ["visionary", "direct", "empathetic", "analytical"]
biases = ["data-driven", "intuitive", "consensus-seeking", "principle-based"]
models = ["transformational", "servant", "command-control", "adaptive"]

# ✅ Generate persona
def generate_persona(name, domain, contribution, bio=None):
    summary = ""
    if bio:
        summary = f"{name} is known for {contribution}. Their work reflects a {random.choice(styles)} approach to {domain.lower()}, often emphasizing {random.choice(biases)} decision-making and {random.choice(models)} leadership."
    else:
        summary = f"{name} shaped the field of {domain.lower()} through their contribution: {contribution}. They are simulated with a {random.choice(styles)} style and {random.choice(models)} leadership model."

    return {
        "name": name,
        "domain": domain,
        "contribution": contribution,
        "persona_description": summary,
        "communication_style": random.choice(styles),
        "decision_bias": random.choice(biases),
        "leadership_model": random.choice(models)
    }

# ✅ Build output
output = []
scraped_names = set()

for profile in scraped:
    name = profile["name"].strip()
    scraped_names.add(name.lower())
    raw_data = raw_index.get(name.lower(), {})
    persona = generate_persona(name, raw_data.get("domain", ""), raw_data.get("contribution", ""), profile.get("bio"))
    output.append(persona)

# ✅ Fallback for missing profiles
for name, raw_data in raw_index.items():
    if name not in scraped_names:
        persona = generate_persona(raw_data["name"], raw_data.get("domain", ""), raw_data.get("contribution", ""), None)
        output.append(persona)
        logging.warning(f"⚠️ Fallback persona generated for {raw_data['name']}")

# ✅ Write output
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4)

logging.info(f"✅ persona_descriptions.json written with {len(output)} entries")