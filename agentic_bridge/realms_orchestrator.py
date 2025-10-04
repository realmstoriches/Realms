import os, re, json, shutil, logging, ast
from datetime import datetime
from collections import defaultdict
from chromadb import Client
from chromadb.config import Settings

# === CONFIGURATION ===
ROOT = r"F:\Realms"
CORES = [os.path.join(ROOT, "realms_core_alpha"), os.path.join(ROOT, "realms_core_beta")]
POOL = os.path.join(ROOT, "agentic_pool")
LOGS = os.path.join(ROOT, "logs", "agent_sync.log")
DASHBOARD_JSON = os.path.join(ROOT, "agentic_dashboard.json")
DASHBOARD_HTML = os.path.join(ROOT, "dashboard.html")
VAULT = os.path.join(ROOT, "envs", ".env.vault")
MONETIZATION_LOGS = os.path.join(ROOT, "logs", "monetization")
SYNDICATION_PAYLOADS = os.path.join(ROOT, "payloads", "syndication")

# === CREWS & ROLES ===
CREWS = {
    "software": ["steve_jobs", "torvalds", "ada_lovelace"],
    "design": ["jony_ive", "don_norman"],
    "hr": ["laszlo_bock"],
    "marketing": ["seth_godin"],
    "ops": ["jeff_bezos"],
}
ROLES = {
    "steve_jobs": "UI Designer",
    "torvalds": "Kernel Engineer",
    "ada_lovelace": "Algorithm Architect",
    "jony_ive": "Product Designer",
    "don_norman": "UX Strategist",
    "laszlo_bock": "HR Director",
    "seth_godin": "Brand Strategist",
    "jeff_bezos": "Operations Lead"
}

# === SETUP ===
os.makedirs(POOL, exist_ok=True)
os.makedirs(os.path.dirname(LOGS), exist_ok=True)
logging.basicConfig(filename=LOGS, level=logging.INFO, format='%(asctime)s - %(message)s')

def log(msg): print(msg); logging.info(msg)

# === CHROMADB ===
chroma_client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=os.path.join(ROOT, "chromadb")))
chroma_collection = chroma_client.get_or_create_collection("agent_memory")

# === DISCOVERY ===
def discover_agents():
    agents = []
    for core in CORES:
        for root, _, files in os.walk(core):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            code = f.read()
                        if any(re.search(sig, code) for sig in [r"\bdef\s+run\(", r"\bdef\s+dispatch\(", r"class\s+Agent"]):
                            crew = infer_crew(path)
                            dual_core = "prime" in file.lower() or "prime" in root.lower()
                            name = os.path.splitext(file)[0]
                            role = infer_role(name)
                            memory = chroma_collection.get(ids=[name]) if chroma_collection.count() else {}
                            agents.append({
                                "name": name,
                                "path": path,
                                "crew": crew,
                                "role": role,
                                "dual_core": dual_core,
                                "memory": memory,
                                "status": "discovered"
                            })
                    except Exception as e:
                        log(f"⚠️ Failed to read {path}: {e}")
    return agents

def infer_crew(path):
    return next((crew for crew, members in CREWS.items() if any(member in path.lower() for member in members)), "fallback")

def infer_role(name):
    return next((role for person, role in ROLES.items() if person in name.lower()), "Fallback Specialist")

# === MONETIZATION & SYNDICATION ===
def parse_monetization():
    monetization = []
    if os.path.exists(MONETIZATION_LOGS):
        for file in os.listdir(MONETIZATION_LOGS):
            with open(os.path.join(MONETIZATION_LOGS, file), "r") as f:
                monetization.append(f.read())
    return monetization

def parse_syndication():
    syndication = []
    if os.path.exists(SYNDICATION_PAYLOADS):
        for file in os.listdir(SYNDICATION_PAYLOADS):
            with open(os.path.join(SYNDICATION_PAYLOADS, file), "r") as f:
                syndication.append(f.read())
    return syndication

# === CREDENTIAL INJECTION ===
def inject_credentials(agent_name):
    if not os.path.exists(VAULT): return {}
    with open(VAULT, "r") as f:
        vault = json.load(f)
    return vault.get(agent_name, {})

# === RESTRUCTURE ===
def restructure_codebase():
    categories = {
        "agents": ["agent", "dispatch", "prime"],
        "tools": ["tool", "util", "prompt"],
        "envs": ["env", "config"],
        "scripts": ["run", "main", "cli"],
        "core": ["core", "executor"]
    }
    for core in CORES:
        for root, _, files in os.walk(core):
            for file in files:
                if file.endswith(".py"):
                    src = os.path.join(root, file)
                    for category, keywords in categories.items():
                        if any(k in file.lower() or k in root.lower() for k in keywords):
                            dst_dir = os.path.join(ROOT, category)
                            os.makedirs(dst_dir, exist_ok=True)
                            shutil.copy2(src, os.path.join(dst_dir, file))
                            break

# === IMPORT REWRITE ===
def rewrite_imports():
    for root, _, files in os.walk(ROOT):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read())
                    updated_lines = []
                    for node in tree.body:
                        if isinstance(node, ast.ImportFrom):
                            old = node.module
                            new = rewrite_path(old)
                            updated_lines.append(f"from {new} import {', '.join([n.name for n in node.names])}")
                        elif isinstance(node, ast.Import):
                            updated_lines.append(f"import {', '.join([n.name for n in node.names])}")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write("\n".join(updated_lines))
                except Exception as e:
                    log(f"⚠️ Failed to rewrite imports in {path}: {e}")

def rewrite_path(old):
    if "realms_core_alpha" in old: return "agents"
    if "promptgen" in old: return "tools.promptgen"
    return "core.executor" if "executor" in old else old

# === CONTAINERIZATION ===
def containerize_agents(agents):
    for agent in agents:
        crew = agent["crew"]
        team = agent["role"].replace(" ", "_").lower()
        dst = os.path.join(POOL, crew, team, agent["name"])
        os.makedirs(dst, exist_ok=True)
        src_dir = os.path.dirname(agent["path"])
        for file in os.listdir(src_dir):
            shutil.copy2(os.path.join(src_dir, file), os.path.join(dst, file))
        agent["container_path"] = dst
        agent["credentials"] = inject_credentials(agent["name"])
        agent["status"] = "containerized"

# === DASHBOARD ===
def build_dashboard(agents, monetization, syndication):
    with open(DASHBOARD_JSON, "w") as f:
        json.dump({
            "timestamp": str(datetime.now()),
            "agents": agents,
            "monetization": monetization,
            "syndication": syndication
        }, f, indent=2)

    html = (
        "<html><head><title>Agentic Dashboard</title></head><body>"
        "<h1>Agent Swarm Health & Roster</h1><table border='1'><tr><th>Name</th><th>Crew</th><th>Role</th><th>Status</th></tr>"
    )
    for agent in agents:
        html += f"<tr><td>{agent['name']}</td><td>{agent['crew']}</td><td>{agent['role']}</td><td>{agent['status']}</td></tr>"
    html += "</table><h2>Monetization Logs</h2><pre>" + "\n".join(monetization) + "</pre>"
    html += "<h2>Syndication Payloads</h2><pre>" + "\n".join(syndication) + "</pre>"
    html += "</body></html>"

    with open(DASHBOARD_HTML, "w", encoding="utf-8") as f:
        f.write(html)

# === MAIN EXECUTION ===
if __name__ == "__main__":
    log("🚀 Starting agent swarm orchestration...")

    # Phase 1: Discovery
    agents = discover_agents()
    log(f"🧠 Discovered {len(agents)} agents")

    # Phase 2: Monetization & Syndication
    monetization = parse_monetization()
    syndication = parse_syndication()
    log(f"💰 Parsed {len(monetization)} monetization logs")
    log(f"📡 Parsed {len(syndication)} syndication payloads")

    # Phase 3: Codebase Restructure
    restructure_codebase()
    log("🧱 Codebase restructured")

    # Phase 4: Import Rewriting
    rewrite_imports()
    log("🔁 Imports rewritten")

    # Phase 5: Containerization
    containerize_agents(agents)
    log("📦 Agents containerized")

    # Phase 6: Dashboard Build
    build_dashboard(agents, monetization, syndication)
    log("📊 Dashboard generated")

    log("🎯 Agent swarm orchestration complete. All systems go.")