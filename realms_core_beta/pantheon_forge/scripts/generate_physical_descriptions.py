import json, random, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)

heights = ["5'6\"", "5'9\"", "6'0\"", "6'2\"", "5'4\""]
builds = ["lean", "athletic", "broad-shouldered", "compact", "graceful"]
styles = ["formal", "minimalist", "eccentric", "techwear", "classic"]
voices = ["warm", "commanding", "gentle", "precise", "resonant"]
presence = ["quiet", "magnetic", "intense", "calm", "assertive"]

for agent in agents:
    agent["physical_description"] = {
        "appearance": f"{random.choice(heights)}, {random.choice(builds)}, {random.choice(styles)} style",
        "voice": random.choice(voices),
        "presence": random.choice(presence)
    }

with open("agent_roster.json", "w", encoding="utf-8") as f:
    json.dump(agents, f, indent=4)

logging.info("✅ agent_roster.json updated with physical descriptions")