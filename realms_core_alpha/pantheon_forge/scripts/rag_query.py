import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Initialize ChromaDB and embedding model
chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./pantheon_vault"))
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Query cognition
def query_agent(agent_name, query_text, top_k=5):
    collection = chroma_client.get_or_create_collection(name=agent_name)
    query_embedding = embedding_model.encode(query_text).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    logging.info(f"🔍 Query results for {agent_name}:")
    for i, doc in enumerate(results["documents"][0]):
        logging.info(f"{i+1}. {doc[:200]}...")
    return results["documents"][0]

# ✅ Main runner
if __name__ == "__main__":
    agent = input("Enter agent name: ").strip()
    query = input("Enter query: ").strip()
    results = query_agent(agent, query)
    print("\n🧠 Top results:")
    for i, doc in enumerate(results):
        print(f"{i+1}. {doc[:300]}...\n")