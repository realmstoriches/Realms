import json

with open("pantheon_forge/company_manifest.json", "r") as f:
    manifest = json.load(f)

agents = manifest["agents"]
tools = manifest["tools"]
crews = manifest["crews"]

print("🧠 Realms Cognitive Empire — Investor Highlights")
print(f"Total Agents: {len(agents)}")
print(f"Toolsets: {[t['name'] for t in tools][:5]}...")
print(f"Active Crews: {[c['crew'] for c in crews][:5]}...")
print("Use cases: Simulation, fallback orchestration, sovereign automation, investor-ready branding\n")