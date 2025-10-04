import json

def load_manifest():
    with open("pantheon_forge/company_manifest.json", "r") as f:
        return json.load(f)