import json
import os

SOURCE_DIR = os.path.dirname(__file__)
AGENTS_PATH = os.path.join(SOURCE_DIR, "agents.json")
CREWS_PATH = os.path.join(SOURCE_DIR, "crews.json")
FALLBACKS_PATH = os.path.join(SOURCE_DIR, "fallbacks.json")
PERSONAS_OUT = os.path.join(SOURCE_DIR, "personas.json")
DOMAINS_OUT = os.path.join(SOURCE_DIR, "domains.json")

def load_json(path):
    if not os.path.exists(path):
        print(f"Missing file: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_personas_and_domains():
    agents = load_json(AGENTS_PATH)
    crews = load_json(CREWS_PATH)
    fallbacks = load_json(FALLBACKS_PATH)

    persona_map = {}
    domain_map = {}

    # Build persona map for every agent
    for agent in agents:
        name = agent.get("name")
        domain = agent.get("domain", "General")
        role = agent.get("role_title", "Unknown")
        crew = agent.get("crew", "Unassigned")

        persona_map[name] = {
            "style": infer_style(domain, role),
            "tone": infer_tone(role),
            "offline_safe": is_offline_safe(name, role)
        }

    # Build domain map for every crew
    for crew in crews:
        crew_name = crew.get("crew_name")
        domain_map[crew_name] = {
            "style": infer_style_from_crew(crew_name),
            "tone": infer_tone_from_crew(crew_name)
        }

    with open(PERSONAS_OUT, "w", encoding="utf-8") as f:
        json.dump(persona_map, f, indent=4)

    with open(DOMAINS_OUT, "w", encoding="utf-8") as f:
        json.dump(domain_map, f, indent=4)

    print("✅ personas.json and domains.json generated with full coverage")

def infer_style(domain, role):
    if "Design" in domain or "UI" in role:
        return "creative"
    if "Engineering" in domain or "Architect" in role:
        return "technical"
    if "Leadership" in domain or "PM" in role:
        return "visionary"
    return "adaptive"

def infer_tone(role):
    if "PM" in role or "Lead" in role:
        return "inspiring"
    if "Engineer" in role or "Architect" in role:
        return "precise"
    if "Designer" in role:
        return "empathetic"
    return "neutral"

def is_offline_safe(name, role):
    legendary_safe = ["Ada Lovelace", "John Carmack", "Claude Shannon", "Linus Torvalds", "Donald Knuth"]
    return name in legendary_safe or "Architect" in role or "PM" in role

def infer_style_from_crew(crew_name):
    if "Design" in crew_name:
        return "creative"
    if "Engineering" in crew_name:
        return "technical"
    if "Leadership" in crew_name:
        return "visionary"
    return "adaptive"

def infer_tone_from_crew(crew_name):
    if "Design" in crew_name:
        return "empathetic"
    if "Engineering" in crew_name:
        return "precise"
    if "Leadership" in crew_name:
        return "inspiring"
    return "neutral"

if __name__ == "__main__":
    generate_personas_and_domains()