import json

def sync_crews(manifest_path="agentic_launchpad/company_manifest.json", mission_path="agentic_launchpad/mission_queue.json"):
    with open(manifest_path) as f:
        manifest = json.load(f)
    with open(mission_path) as f:
        missions = json.load(f)

    existing = {c["crew_name"] for c in manifest.get("crews", [])}
    new_crews = {m["assigned_crew"] for m in missions if m.get("assigned_crew")} - existing

    for crew in new_crews:
        manifest["crews"].append({"crew_name": crew})

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"✅ Synced crews: {', '.join(new_crews) if new_crews else 'No new crews found'}")