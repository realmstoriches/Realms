from manifest_loader import load_manifest

def get_fallback_agent(role_title, exclude_crew):
    manifest = load_manifest()
    for role in manifest["expanded_roles"]:
        if role["role_title"] == role_title and role["crew"] != exclude_crew:
            return role["agent_name"]
    return None