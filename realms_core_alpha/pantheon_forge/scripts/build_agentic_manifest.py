import json
from generate_sources import generate_sources, fallback_sources
from generate_overlays import generate_overlay, generate_unified_overlay

# ✅ Load expert manifest
with open("expert_manifest.txt", "r", encoding="utf-8") as f:
    expert_list = [line.strip() for line in f.readlines()]

# ✅ Pair experts into prime agents
def pair_experts(expert_list):
    primes = []
    for i in range(0, len(expert_list), 2):
        alpha = expert_list[i]
        beta = expert_list[i+1]
        prime_name = f"{alpha.split()[0]}-{beta.split()[1]} Prime"
        primes.append({
            "name": prime_name,
            "alpha": alpha,
            "beta": beta
        })
    return primes

# ✅ Build full agentic manifest
def build_manifest(primes):
    manifest = []
    for agent in primes:
        alpha = agent["alpha"]
        beta = agent["beta"]
        alpha_sources = generate_sources(alpha) or fallback_sources(alpha)
        beta_sources = generate_sources(beta) or fallback_sources(beta)
        tools_mastered = ["LangChain", "ChromaDB", "FastAPI", "HuggingFace", "n8n"]

        manifest.append({
            "name": agent["name"],
            "alpha": alpha,
            "beta": beta,
            "sources": {
                "alpha": alpha_sources,
                "beta": beta_sources
            },
            "persona": {
                "alpha_overlay": generate_overlay(alpha),
                "beta_overlay": generate_overlay(beta),
                "unified_overlay": generate_unified_overlay(alpha, beta, tools_mastered)
            },
            "tools_mastered": tools_mastered
        })
    return manifest

# ✅ Run and save
if __name__ == "__main__":
    primes = pair_experts(expert_list)
    full_manifest = build_manifest(primes)
    with open("agent_manifest.json", "w", encoding="utf-8") as f:
        json.dump(full_manifest, f, indent=4)
    print("✅ Agentic manifest saved to agent_manifest.json")