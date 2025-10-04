import json
import os

BASE_DIR = os.path.dirname(__file__)
AGENT_MANIFEST = os.path.join(BASE_DIR, "agent_manifest.json")
PRICING_MODEL = os.path.join(BASE_DIR, "pricing_model.json")
BUSINESS_PLAN = os.path.join(BASE_DIR, "business_plan.json")  # Optional

def ingest_agents():
    if not os.path.exists(AGENT_MANIFEST):
        print("❌ agent_manifest.json not found.")
        return []
    with open(AGENT_MANIFEST, "r", encoding="utf-8") as f:
        data = json.load(f)
    agents = data.get("new_agents", [])
    print(f"👥 Ingested {len(agents)} agents.")
    return agents

def ingest_pricing():
    if not os.path.exists(PRICING_MODEL):
        print("❌ pricing_model.json not found.")
        return {}
    with open(PRICING_MODEL, "r", encoding="utf-8") as f:
        pricing = json.load(f)
    print("💸 Pricing model loaded.")
    return pricing

def ingest_business_plan():
    if not os.path.exists(BUSINESS_PLAN):
        print("⚠️ No business_plan.json found. Skipping.")
        return {}
    with open(BUSINESS_PLAN, "r", encoding="utf-8") as f:
        plan = json.load(f)
    print("📈 Business plan directives loaded.")
    return plan

def run_ingestion():
    print("🚀 Starting Realms ingestion sequence...")
    agents = ingest_agents()
    pricing = ingest_pricing()
    plan = ingest_business_plan()

    # Save to dispatch-ready format
    output_path = os.path.join(BASE_DIR, "dispatch_manifest.json")
    manifest = {
        "agents": agents,
        "pricing": pricing,
        "business_plan": plan
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)
    print(f"✅ Dispatch manifest created: {output_path}")

if __name__ == "__main__":
    run_ingestion()