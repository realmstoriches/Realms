import json
import requests
import logging
import time
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Initialize ChromaDB
chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./pantheon_vault"))
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Chunking logic
def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# ✅ Scrape and embed
def ingest_agent(agent):
    name = agent["name"]
    alpha = agent["alpha"]
    beta = agent["beta"]
    sources = agent["sources"]["alpha"] + agent["sources"]["beta"]

    documents = []
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                chunks = chunk_text(response.text)
                for chunk in chunks:
                    embedding = embedding_model.encode(chunk)
                    documents.append({
                        "agent": name,
                        "chunk": chunk,
                        "embedding": embedding.tolist()
                    })
                logging.info(f"✅ Ingested {len(chunks)} chunks from {url}")
            else:
                logging.warning(f"⚠️ Failed to fetch {url}: {response.status_code}")
        except Exception as e:
            logging.warning(f"⚠️ Error fetching {url}: {e}")
        time.sleep(1)

    # ✅ Store in ChromaDB
    collection = chroma_client.get_or_create_collection(name=name)
    for i, doc in enumerate(documents):
        collection.add(
            documents=[doc["chunk"]],
            embeddings=[doc["embedding"]],
            ids=[f"{name}_{i}"]
        )
    logging.info(f"🧠 Stored {len(documents)} chunks for {name}")

# ✅ Main runner
if __name__ == "__main__":
    with open("agent_manifest.json", "r", encoding="utf-8") as f:
        agents = json.load(f)

    for agent in agents:
        ingest_agent(agent)

    logging.info("✅ All agents ingested into ChromaDB vaults")