import json, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)
with open("dual_brain_manifest.json", "r", encoding="utf-8") as f:
    pairs = json.load(f)

agent_index = {a["name"]: a for a in agents}
fused = []

for pair in pairs:
    alpha = agent_index.get(pair["alpha"])
    beta = agent_index.get(pair["beta"])
    if alpha and beta:
        fused.append({
            "agent_pair_id": pair["agent_pair_id"],
            "crew": pair["crew"],
            "fused_persona": f"{alpha['persona_description']} Combined with {beta['persona_description']}",
            "combined_tools": list(set(alpha["tools_required"] + beta["tools_required"])),
            "hybrid_leadership_model": f"{alpha['leadership_model']} + {beta['leadership_model']}",
            "fallback_logic": pair["fallback_pair"]
        })

with open("fused_agent_profiles.json", "w", encoding="utf-8") as f:
    json.dump(fused, f, indent=4)

logging.info(f"✅ fused_agent_profiles.json written with {len(fused)} entries")