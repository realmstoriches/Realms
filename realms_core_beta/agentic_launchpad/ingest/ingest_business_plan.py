import json
import os

ROOT_DIR = os.path.abspath("F:/realms_core/agentic_launchpad")
PLAN_PATH = os.path.join(ROOT_DIR, "data", "business_plan.json")
CHROMA_DB_PATH = os.path.join(ROOT_DIR, "chroma_db", "business_plan_vector.json")

def load_plan():
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def vectorize_plan(plan):
    # Simplified vectorization: flatten into key-value strings
    return [f"{k}: {v}" if not isinstance(v, dict) else f"{k}: {json.dumps(v)}" for k, v in plan.items()]

def save_to_chroma(vectorized):
    os.makedirs(os.path.dirname(CHROMA_DB_PATH), exist_ok=True)
    with open(CHROMA_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(vectorized, f, indent=4)
    print("✅ Business plan ingested into chroma_db")

def ingest():
    plan = load_plan()
    vectorized = vectorize_plan(plan)
    save_to_chroma(vectorized)

if __name__ == "__main__":
    ingest()