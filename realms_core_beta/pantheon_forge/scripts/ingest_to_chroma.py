import json
import logging
import chromadb

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

roster_file = "agent_roster.json"
roster = json.load(open(roster_file, "r", encoding="utf-8"))

client = chromadb.Client()
collection = client.get_or_create_collection(name="agentic_minds")

for agent in roster:
    content = f"{agent['persona_description']} {agent['scraped_content']}"
    metadata = {
        "name": agent["name"],
        "domain": agent["domain"],
        "role": agent["role_title"],
        "agent_id": agent["agent_id"],
        "communication_style": agent["communication_style"],
        "leadership_model": agent["leadership_model"]
    }
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[agent["agent_id"]]
    )
    agent["knowledge_vector_id"] = agent["agent_id"]
    logging.info(f"🧠 Ingested {agent['name']}")

# ✅ Update roster with vector IDs
with open("agent_roster.json", "w", encoding="utf-8") as f:
    json.dump(roster, f, indent=4)

logging.info("✅ ChromaDB ingestion complete and agent_roster.json updated")