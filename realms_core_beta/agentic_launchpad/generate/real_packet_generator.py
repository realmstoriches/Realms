import json
import os

SOURCE_DIR = os.path.dirname(__file__)
AGENTS_PATH = os.path.join(SOURCE_DIR, "agents.json")
CREWS_PATH = os.path.join(SOURCE_DIR, "crews.json")
FALLBACKS_PATH = os.path.join(SOURCE_DIR, "fallbacks.json")
PERSONAS_PATH = os.path.join(SOURCE_DIR, "personas.json")
DOMAINS_PATH = os.path.join(SOURCE_DIR, "domains.json")
PACKET_DIR = os.path.join(SOURCE_DIR, "real_packets")

def load_json(path):
    if not os.path.exists(path):
        print(f"Missing file: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_packets():
    agents = load_json(AGENTS_PATH)
    crews = load_json(CREWS_PATH)
    fallbacks = load_json(FALLBACKS_PATH)
    personas = load_json(PERSONAS_PATH)
    domains = load_json(DOMAINS_PATH)

    os.makedirs(PACKET_DIR, exist_ok=True)

    crew_map = {}
    for agent in agents:
        crew = agent.get("crew")
        role = agent.get("role_title")
        name = agent.get("name")
        domain = agent.get("domain", "General")
        persona = personas.get(name, {})
        if crew and role and name:
            crew_map.setdefault(crew, {}).setdefault(role, []).append({
                "name": name,
                "domain": domain,
                "persona": persona
            })

    fallback_map = {}
    for entry in fallbacks:
        role = entry.get("role_title")
        fallback_map[role] = entry.get("fallbacks", [])

    for crew in crews:
        crew_name = crew.get("crew_name")
        roles = crew_map.get(crew_name, {})
        packet = {
            "crew_name": crew_name,
            "mission_scope": f"Real mission packet for {crew_name}",
            "agents": [],
            "fallbacks": [],
            "domains": set(),
            "persona_overlay": {},
            "dispatch_logic": {
                "primary": crew_name,
                "fallback": [],
                "twin_origin": f"pantheon_twin/{crew_name}",
                "offline_safe": []
            }
        }

        for role, members in roles.items():
            for agent in members:
                packet["agents"].append({
                    "role_title": role,
                    "agent_name": agent["name"],
                    "domain": agent["domain"],
                    "persona": agent["persona"]
                })
                packet["domains"].add(agent["domain"])
                if agent["persona"].get("offline_safe"):
                    packet["dispatch_logic"]["offline_safe"].append(agent["name"])
            for fallback in fallback_map.get(role, []):
                packet["fallbacks"].append({
                    "role_title": role,
                    "fallback_agent": fallback
                })
                packet["dispatch_logic"]["fallback"].append(fallback)

        packet["domains"] = sorted(list(packet["domains"]))
        packet["persona_overlay"] = {
            "crew_style": domains.get(crew_name, {}).get("style", "adaptive"),
            "tone": domains.get(crew_name, {}).get("tone", "neutral")
        }

        out_path = os.path.join(PACKET_DIR, f"real_packet_{crew_name}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(packet, f, indent=4)

    print("✅ Real mission packets generated in real_packets/")

if __name__ == "__main__":
    generate_packets()