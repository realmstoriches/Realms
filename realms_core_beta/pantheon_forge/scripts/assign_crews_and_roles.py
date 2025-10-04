import json, logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with open("dual_brain_manifest.json", "r", encoding="utf-8") as f:
    pairs = json.load(f)
with open("agent_roster.json", "r", encoding="utf-8") as f:
    agents = json.load(f)

agent_index = {a["name"]: a for a in agents}
crew_manifest = []

for pair in pairs:
    alpha = agent_index.get(pair["alpha"])
    beta = agent_index.get(pair["beta"])
    if alpha and beta:
        crew_manifest.append({
            "crew_name": pair["crew"],
            "mission_brief": f"Deploy {alpha['domain']} and {beta['domain']} expertise to solve strategic challenges.",
            "agent_roles": {
                "alpha": {"name": alpha["name"], "role": alpha["role_title"]},
                "beta": {"name": beta["name"], "role": beta["role_title"]}
            },
            "tool_access": list(set(alpha["tools_required"] + beta["tools_required"])),
            "simulation_flags": {
                "fallback": pair["fallback_pair"],
                "escalation": "use fused persona if both agents fail"
            }
        })

with open("crew_manifest.json", "w", encoding="utf-8") as f:
    json.dump(crew_manifest, f, indent=4)

logging.info(f"✅ crew_manifest.json written with {len(crew_manifest)} crews")