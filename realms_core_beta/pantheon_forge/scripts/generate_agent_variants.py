import json, random, uuid, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)

styles = ["visionary", "direct", "empathetic", "analytical"]
biases = ["data-driven", "intuitive", "consensus-seeking", "principle-based"]
models = ["transformational", "servant", "command-control", "adaptive"]

variants = []
for agent in agents:
    for _ in range(2):
        variant = {
            "variant_id": str(uuid.uuid4())[:8],
            "origin": agent["name"],
            "mutation": {
                "communication_style": random.choice(styles),
                "decision_bias": random.choice(biases),
                "leadership_model": random.choice(models)
            },
            "vector_linkage": agent["agent_id"],
            "status": "scalable",
            "simulation_ready": True
        }
        variants.append(variant)

with open("agent_variants.json", "w", encoding="utf-8") as f:
    json.dump(variants, f, indent=4)

logging.info(f"✅ agent_variants.json written with {len(variants)} variants")