import os, json, logging
from chromadb import PersistentClient
from chromadb.config import Settings
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

logging.basicConfig(level=logging.INFO)

# Initialize Chroma client
chroma_client = PersistentClient(path="chroma_db")
# Use Ollama-compatible embedding model (e.g., all-MiniLM-L6-v2)
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create collection
collection = chroma_client.get_or_create_collection(name="realms_knowledge", embedding_function=embedding_fn)

# Define sources
sources = {
    "real_minds": "pantheon_forge/real_minds.json",
    "tools": "pantheon_forge/tools_manifest.json",
    "personas": "pantheon_forge/persona_descriptions.json",
    "knowledge": "pantheon_forge/KNOWLEDGE_SOURCES.json"
}

# Ingest each source
for label, path in sources.items():
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for i, item in enumerate(data):
            text = json.dumps(item) if isinstance(item, dict) else str(item)
            collection.add(
                documents=[text],
                metadatas=[{"source": label}],
                ids=[f"{label}_{i}"]
            )
        logging.info(f"✅ Ingested {len(data)} items from {label}")
    except Exception as e:
        logging.warning(f"⚠️ Failed to ingest {label}: {e}")

# Persist to disk
# chroma_client.persist()
logging.info("🧠 Chroma vector store updated and saved to chroma_db/")