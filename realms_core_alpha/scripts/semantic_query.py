from chromadb import PersistentClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

client = PersistentClient(path="chroma_db")
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = client.get_or_create_collection(name="realms_knowledge", embedding_function=embedding_fn)

def query_concept(concept: str, top_k=5):
    results = collection.query(query_texts=[concept], n_results=top_k)
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        print(f"🔹 {meta['source']}: {doc[:200]}...\n")

if __name__ == "__main__":
    query_concept("fallback logic for simulation")