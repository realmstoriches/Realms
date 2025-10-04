import json
import logging
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

files = {
    "raw": "real_minds.json",
    "urls": "validated_urls.json",
    "bios": "mind_profiles.json",
    "personas": "persona_descriptions.json",
    "tools": "tools_manifest.json"
}

# ✅ Load all inputs
data = {k: json.load(open(v, "r", encoding="utf-8")) for k, v in files.items()}
bios_index = {p["name"].lower(): p for p in data["bios"]}
persona_index = {p["name"].lower(): p for p in data["personas"]}
tools_index = data["tools"]
urls_index = data["urls"]

roster = []

for mind in data["raw"]:
    name = mind["name"]
    key = name.lower()
    agent_id = str(uuid.uuid4())[:8]
    persona = persona_index.get(key, {})
    bio = bios_index.get(key, {})
    urls = urls_index.get(key.replace(" ", "_"), [])
    tools = tools_index.get(name, {})

    roster.append({
        "agent_id": agent_id,
        "name": name,
        "domain": mind.get("domain", ""),
        "role_title": f"{mind.get('domain', '')} Specialist",
        "contribution": mind.get("contribution", ""),
        "status": "active",
        "assigned_module": mind.get("domain", "").lower().replace(" ", "_"),
        "fallback_role": "generalist",
        "tools_required": tools.get("tools", []),
        "preferred_stack": tools.get("preferred_stack", "Agile"),
        "validated_urls": urls,
        "scraped_content": bio.get("bio", ""),
        "quotes": bio.get("quotes", []),
        "knowledge_vector_id": None,
        "persona_description": persona.get("persona_description", ""),
        "communication_style": persona.get("communication_style", ""),
        "decision_bias": persona.get("decision_bias", ""),
        "leadership_model": persona.get("leadership_model", ""),
        "contract_type": "perpetual",
        "availability": "mission-specific",
        "simulation_ready": True,
        "fallback_logic": "use persona + quotes if vector fails"
    })

with open("agent_roster.json", "w", encoding="utf-8") as f:
    json.dump(roster, f, indent=4)

logging.info(f"✅ agent_roster.json written with {len(roster)} agents")