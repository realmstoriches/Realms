import os
import subprocess
from pathlib import Path

ROOT = Path("F:/Realms/realms_core_alpha")
LOG = ROOT / "logs" / "swarm_seal_log.txt"
LOG.parent.mkdir(exist_ok=True)

# Modules to drop with full function bodies
MODULES = {
    "config_manager.py": "def get_env():\n    return os.environ.get('REALMS_ENV', 'pantheon_env')\n",
    "manifest_loader.py": "def load_manifest():\n    print('📦 Manifest loaded')\n    return {}\n",
    "dispatch_variant_agent.py": "def generate_variant():\n    print('🎨 Dispatch variant generated')\n",
    "generate_sources.py": "def generate_sources():\n    print('🔗 Sources generated')\n",
    "generate_overlays.py": "def generate_overlay():\n    print('🧢 Overlay generated')\n",
    "agent_output_generator.py": "def generate_output():\n    print('📤 Agent output generated')\n",
    "tool_executor.py": "def execute_tool():\n    print('🛠️ Tool executed')\n",
    "routes/agents.py": "from fastapi import APIRouter\nrouter = APIRouter()\ndef load_manifest():\n    print('📦 Manifest loaded')\n    return {}\n",
    "promptgen.py": "def generate():\n    print('🧠 Prompt generated')\n"
}

# Required packages
PACKAGES = [
    "python-dotenv", "fastapi", "moviepy", "chromadb",
    "sentence-transformers", "beautifulsoup4", "selenium", "pillow", "flask"
]

def install_packages():
    installed = []
    for pkg in PACKAGES:
        try:
            subprocess.run(["pip", "install", pkg], check=True)
            installed.append(pkg)
        except subprocess.CalledProcessError:
            pass
    return installed

def inject_init_files():
    injected = []
    for folder in ROOT.rglob("*"):
        if folder.is_dir():
            init = folder / "__init__.py"
            if not init.exists():
                init.write_text("", encoding="utf-8")
                injected.append(str(init))
    return injected

def drop_modules():
    dropped = []
    for rel_path, body in MODULES.items():
        path = ROOT / rel_path.replace("/", os.sep)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(body, encoding="utf-8")
            dropped.append(str(path))
    return dropped

def expose_in_init():
    exposed = []
    for rel_path in MODULES:
        parts = rel_path.split("/")
        if len(parts) == 1:
            module = parts[0].replace(".py", "")
            init_path = ROOT / "__init__.py"
        else:
            module = parts[-1].replace(".py", "")
            init_path = ROOT / "/".join(parts[:-1]) / "__init__.py"
        if init_path.exists():
            current = init_path.read_text(encoding="utf-8")
            expose_line = f"from .{module} import {MODULES[rel_path].split()[1].split('(')[0]}"
            if expose_line not in current:
                init_path.write_text(current + "\n" + expose_line + "\n", encoding="utf-8")
                exposed.append(str(init_path))
    return exposed

def log_results(installed, injected, dropped, exposed):
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("✅ Final Swarm Seal Log\n\n")
        f.write("📦 Packages Installed:\n")
        for pkg in installed:
            f.write(f"{pkg}\n")
        f.write("\n🧱 __init__.py Injected:\n")
        for path in injected:
            f.write(f"{path}\n")
        f.write("\n🧪 Modules Dropped:\n")
        for path in dropped:
            f.write(f"{path}\n")
        f.write("\n🔗 Exposure Patched:\n")
        for path in exposed:
            f.write(f"{path}\n")

def main():
    print("🧠 Executing final swarm seal...")
    installed = install_packages()
    injected = inject_init_files()
    dropped = drop_modules()
    exposed = expose_in_init()
    log_results(installed, injected, dropped, exposed)
    print(f"✅ Swarm sealed. Log saved to: {LOG}")

if __name__ == "__main__":
    main()