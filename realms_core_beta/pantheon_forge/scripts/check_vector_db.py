import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(anonymized_telemetry=False, persist_directory="./chroma_db"))
collections = client.list_collections()

total = 0
for col in collections:
    count = len(client.get_collection(col.name).get()["ids"])
    print(f"{col.name}: {count} vectors")
    total += count

print(f"\n✅ Total vectors ingested: {total}")
