import json, logging, os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define source files
source_files = {
    "agents": "agent_roster.json",
    "agent_variants": "agent_variants.json",
    "crews": "crew_manifest.json",
    "dual_brains": "dual_brain_manifest.json",
    "expanded_roles": "expanded_role_matrix.json",
    "org_roles": "full_role_matrix.json",
    "fused_profiles": "fused_agent_profiles.json",
    "role_assignments": "role_assignments.json",
    "teams": "team_roster.json",
    "tools": "tools_manifest.json",
    "personas": "persona_descriptions.json",
    "minds": "mind_profiles.json",
    "real_minds": "real_minds.json",
    "validated_links": "validated_urls.json",
    "knowledge_sources": "KNOWLEDGE_SOURCES.json"
}

# Optional: convert expert_manifest.txt to JSON if needed
expert_manifest_path = "expert_manifest.txt"
if os.path.exists(expert_manifest_path):
    with open(expert_manifest_path, "r", encoding="utf-8") as f:
        experts = [{"name": line.strip()} for line in f if line.strip()]
else:
    experts = []

# Merge all files
manifest = {}
for key, filename in source_files.items():
    try:
        with open(filename, "r", encoding="utf-8") as f:
            manifest[key] = json.load(f)
        logging.info(f"✅ Loaded {filename} into '{key}'")
    except Exception as e:
        logging.warning(f"⚠️ Failed to load {filename}: {e}")
        manifest[key] = []

# Add expert manifest
manifest["expert_manifest"] = experts

# Write unified manifest
with open("company_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=4)

logging.info("🎯 company_manifest.json written with full system integration")