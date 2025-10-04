import json, random, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)

# Shuffle and pair
random.shuffle(agents)
pairs = []
for i in range(0, 200, 2):
    alpha, beta = agents[i], agents[i+1]
    pair = {
        "agent_pair_id": f"DB-{i//2+1:03}",
        "alpha": alpha["name"],
        "beta": beta["name"],
        "crew": f"Crew_Alpha_{i//2+1}",
        "status": "active",
        "fallback_pair": [agents[(i+2)%len(agents)]["name"], agents[(i+3)%len(agents)]["name"]]
    }
    pairs.append(pair)

with open("dual_brain_manifest.json", "w", encoding="utf-8") as f:
    json.dump(pairs, f, indent=4)

logging.info(f"✅ dual_brain_manifest.json written with {len(pairs)} pairs")