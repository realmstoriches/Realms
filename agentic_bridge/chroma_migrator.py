import os, json
from chromadb import HttpClient

LEGACY_PATH = r"F:\Realms\chromadb"
HTTP_CLIENT = HttpClient(host="localhost", port=8000)
TARGET_COLLECTION = HTTP_CLIENT.get_or_create_collection("agent_memory")

def migrate_legacy_data():
    for root, _, files in os.walk(LEGACY_PATH):
        for file in files:
            if file.endswith(".json") or file.endswith(".parquet"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    for item in data.get("items", []):
                        TARGET_COLLECTION.add(
                            ids=[item["id"]],
                            documents=[item["document"]],
                            metadatas=[item.get("metadata", {})]
                        )
                    print(f"✅ Migrated: {file}")
                except Exception as e:
                    print(f"⚠️ Failed to migrate {file}: {e}")

if __name__ == "__main__":
    migrate_legacy_data()