import json
import random

# ✅ Domain pools for overlay generation
domains = [
    "AI Engineering", "Systems Architecture", "Security", "UX Design", "DevOps",
    "Hardware", "Theoretical CS", "Product Strategy", "Finance", "Governance"
]

tools = ["LangChain", "ChromaDB", "FastAPI", "HuggingFace", "n8n"]

# ✅ Generate persona overlays
def generate_overlay(name, domain=None):
    if not domain:
        domain = random.choice(domains)
    return f"{name} is a domain expert in {domain}, known for precision, adaptability, and strategic execution."

def generate_unified_overlay(alpha, beta, tools_mastered):
    return (
        f"Unified persona combines {alpha} and {beta}'s cognition, enriched by mastery of tools: "
        f"{', '.join(tools_mastered)}. Capable of autonomous decision-making, simulation, and founder-bound governance."
    )

# ✅ Main runner
if __name__ == "__main__":
    with open("prime_agents.json", "r", encoding="utf-8") as f:
        prime_agents = json.load(f)

    overlays = {}
    for agent in prime_agents:
        alpha = agent["alpha"]
        beta = agent["beta"]
        tools_mastered = tools
        overlays[agent["name"]] = {
            "alpha_overlay": generate_overlay(alpha),
            "beta_overlay": generate_overlay(beta),
            "unified_overlay": generate_unified_overlay(alpha, beta, tools_mastered),
            "tools_mastered": tools_mastered
        }

    with open("agent_overlays.json", "w", encoding="utf-8") as f:
        json.dump(overlays, f, indent=4)

    print("✅ Overlays generated and saved to agent_overlays.json")