import json

def auto_fill_missing_roles(required_roles, manifest_path="agentic_launchpad/company_manifest.json"):
    with open(manifest_path) as f:
        manifest = json.load(f)

    existing_roles = {r["role_title"] for r in manifest.get("expanded_roles", [])}
    missing = set(required_roles) - existing_roles

    for role in missing:
        manifest["expanded_roles"].append({
            "agent_name": f"Auto_{role.replace(' ', '_')}",
            "role_title": role,
            "crew": "Fallback_Crew"
        })

    if missing and "Fallback_Crew" not in [c["crew_name"] for c in manifest.get("crews", [])]:
        manifest["crews"].append({"crew_name": "Fallback_Crew"})

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"✅ Auto-filled missing roles: {', '.join(missing) if missing else 'None'}")