import os, re, json

ROOT = r"F:\Realms"
CORES = ["realms_core_alpha", "realms_core_beta"]
SUBDIRS = [
    "", "agentic_launchpad", "autopilot", "chroma_db", "pantheon_forge",
    "realms_agentic_core", "scripts", "super_image"
]
OUTPUT = os.path.join(ROOT, "agentic_bridge", "discovered_agents.json")

def scan():
    agents = []
    for core in CORES:
        for sub in SUBDIRS:
            path = os.path.join(ROOT, core, sub)
            if not os.path.exists(path): continue
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".py"):
                        full = os.path.join(root, file)
                        try:
                            with open(full, "r", encoding="utf-8") as f:
                                code = f.read()
                            if any(re.search(sig, code) for sig in [r"\bdef\s+run\(", r"\bdef\s+dispatch\(", r"class\s+Agent"]):
                                agents.append({"name": file.replace(".py", ""), "path": full})
                        except Exception:
                            continue
    with open(OUTPUT, "w") as f:
        json.dump(agents, f, indent=2)
    print(f"✅ Discovered {len(agents)} agents")

if __name__ == "__main__":
    scan()