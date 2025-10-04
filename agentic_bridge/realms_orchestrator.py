import os, re, json, shutil, logging, ast, subprocess
from datetime import datetime
from collections import defaultdict

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
CHROMA_PATH = os.path.join(ROOT, "chromadb")

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

# === CHROMADB AUTO-HEAL ===
def get_chroma_client():
    try:
        from chromadb import Client
        from chromadb.config import Settings
        return Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_PATH))
    except Exception as e:
        log("⚠️ Legacy Chroma config failed. Switching to HTTP client...")
        try:
            from chromadb import HttpClient
            return HttpClient(host="localhost", port=8000)
        except Exception as e2:
            log(f"❌ ChromaDB connection failed: {e2}")
            return None

chroma_client = get_chroma_client()
chroma_collection = chroma_client.get_or_create_collection("agent_memory") if chroma_client else None

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
                            memory = chroma_collection.get(ids=[name]) if chroma_collection else {}
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
def parse_logs(folder):
    logs = []
    if os.path.exists(folder):
        for file in os.listdir(folder):
            try:
                with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                    logs.append(f.read())
            except Exception as e:
                log(f"⚠️ Failed to read log {file}: {e}")
    return logs

# === CREDENTIAL INJECTION ===
def inject_credentials(agent_name):
    if not os.path.exists(VAULT): return {}
    try:
        with open(VAULT, "r") as f:
            vault = json.load(f)
        return vault.get(agent_name, {})
    except Exception as e:
        log(f"⚠️ Vault read failed: {e}")
        return {}

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
            try:
                shutil.copy2(os.path.join(src_dir, file), os.path.join(dst, file))
            except Exception as e:
                log(f"⚠️ Failed to copy {file} for {agent['name']}: {e}")
        agent["container_path"] = dst
        agent["credentials"] = inject_credentials(agent["name"])
        agent["status"] = "containerized"

# === DASHBOARD ===
# === DASHBOARD CONTINUED ===
def build_dashboard(agents, monetization, syndication):
    with open(DASHBOARD_JSON, "w") as f:
        json.dump({
            "timestamp": str(datetime.now()),
            "agents": agents,
            "monetization": monetization,
            "syndication": syndication
        }, f, indent=2)

    html = (
        "<html><head><title>Agentic Dashboard</title><style>"
        "body{font-family:sans-serif;background:#111;color:#eee;padding:20px;}table{width:100%;border-collapse:collapse;}th,td{border:1px solid #444;padding:8px;}th{background:#222;}tr:nth-child(even){background:#1a1a1a;}"
        "</style></head><body>"
    )
    html += "<h1>🧠 Agent Swarm Health & Roster</h1><table><tr><th>Name</th><th>Crew</th><th>Role</th><th>Status</th><th>Dual-Core</th></tr>"
    for agent in agents:
        html += f"<tr><td>{agent['name']}</td><td>{agent['crew']}</td><td>{agent['role']}</td><td>{agent['status']}</td><td>{'✅' if agent['dual_core'] else '—'}</td></tr>"
    html += "</table>"

    html += "<h2>💰 Monetization Logs</h2><pre style='background:#222;padding:10px;border:1px solid #444;'>"
    html += "\n\n".join(monetization) if monetization else "No monetization logs found."
    html += "</pre>"

    html += "<h2>📡 Syndication Payloads</h2><pre style='background:#222;padding:10px;border:1px solid #444;'>"
    html += "\n\n".join(syndication) if syndication else "No syndication payloads found."
    html += "</pre>"

    html += "<h2>🧩 Credential Mesh Status</h2><table><tr><th>Agent</th><th>Keys Injected</th></tr>"
    for agent in agents:
        creds = agent.get("credentials", {})
        html += f"<tr><td>{agent['name']}</td><td>{', '.join(creds.keys()) if creds else '—'}</td></tr>"
    html += "</table>"

    html += "<h2>📦 Container Paths</h2><table><tr><th>Agent</th><th>Path</th></tr>"
    for agent in agents:
        html += f"<tr><td>{agent['name']}</td><td>{agent.get('container_path', '—')}</td></tr>"
    html += "</table>"

    html += "<h2>🛠️ Future Modules</h2><ul>"
    html += "<li>Dispatch Supervisor</li><li>Agentic Watchdog</li><li>Revenue Tracker</li><li>Credential Rotator</li><li>Live API Feed</li>"
    html += "</ul>"

    html += "</body></html>"

    with open(DASHBOARD_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    log(f"📊 Dashboard written to {DASHBOARD_HTML}")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    log("🚀 Starting agent swarm orchestration...")

    # Phase 1: Discovery
    agents = discover_agents()
    log(f"🧠 Discovered {len(agents)} agents")

    # Phase 2: Monetization & Syndication
    monetization = parse_logs(MONETIZATION_LOGS)
    syndication = parse_logs(SYNDICATION_PAYLOADS)
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
    log("🎯 Agent swarm orchestration complete. All systems go.")

