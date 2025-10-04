import json

with open("pantheon_forge/dual_brain_manifest.json", "r") as f:
    duals = json.load(f)

print("```mermaid\nflowchart TD")
for pair in duals:
    print(f"{pair['alpha']} -->|Fallback| {pair['beta']}")
print("```")