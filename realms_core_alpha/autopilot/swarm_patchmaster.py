import os
import re
import subprocess
from pathlib import Path

ROOT = Path("F:/Realms/realms_core_alpha")
LOG = ROOT / "logs" / "swarm_patchmaster_log.txt"
LOG.parent.mkdir(exist_ok=True)

# Known third-party packages to validate
THIRD_PARTY = {
    "dotenv": "python-dotenv",
    "fastapi": "fastapi",
    "moviepy": "moviepy",
    "chromadb": "chromadb",
    "sentence_transformers": "sentence-transformers",
    "bs4": "beautifulsoup4",
    "selenium": "selenium",
    "PIL": "pillow",
    "flask": "flask",
    "email.mime.text": None,
    "email.mime.multipart": None,
    "http.server": None,
    "urllib.parse": None,
    "collections": None,
    "random": None,
    "datetime": None,
    "pathlib": None
}

def ensure_init_files():
    sealed = []
    for folder in ROOT.rglob("*"):
        if folder.is_dir():
            init = folder / "__init__.py"
            if not init.exists():
                init.write_text("", encoding="utf-8")
                sealed.append(str(init))
    return sealed

def install_missing_packages():
    installed = []
    for module, pip_name in THIRD_PARTY.items():
        if pip_name:
            try:
                __import__(module.split(".")[0])
            except ImportError:
                subprocess.run(["pip", "install", pip_name])
                installed.append(pip_name)
    return installed

def generate_stub(path, func_name):
    stub = f"def {func_name}():\n    print(\"🧪 Stub agent {func_name} activated\")\n"
    path.write_text(stub, encoding="utf-8")
    return str(path)

def scan_for_unresolved_imports():
    unresolved = []
    for file in ROOT.rglob("*.py"):
        try:
            code = file.read_text(encoding="utf-8")
        except Exception:
            continue
        for match in re.findall(r'from ([\w\.]+) import ([\w_]+)', code):
            module_path = ROOT / Path(match[0].replace(".", "/") + ".py")
            if not module_path.exists():
                unresolved.append((file, match[0], match[1]))
    return unresolved

def generate_stubs_for_unresolved(unresolved):
    stubbed = []
    for _, module, symbol in unresolved:
        if module.startswith("realms_agentic_core") or module.startswith("agentic_launchpad"):
            path = ROOT / Path(module.replace(".", "/") + ".py")
            if not path.exists():
                stubbed.append(generate_stub(path, symbol))
    return stubbed

def log_results(sealed, installed, unresolved, stubbed):
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("✅ Final Swarm Patchmaster Log\n\n")
        f.write("🧱 __init__.py Injected:\n")
        for path in sealed:
            f.write(f"{path}\n")
        f.write("\n📦 Packages Installed:\n")
        for pkg in installed:
            f.write(f"{pkg}\n")
        f.write("\n❌ Unresolved Imports:\n")
        for file, module, symbol in unresolved:
            f.write(f"{file.name}: from {module} import {symbol} → NOT FOUND\n")
        f.write("\n🧪 Stub Agents Generated:\n")
        for stub in stubbed:
            f.write(f"{stub}\n")

def main():
    print("🧠 Executing final swarm patch...")
    sealed = ensure_init_files()
    installed = install_missing_packages()
    unresolved = scan_for_unresolved_imports()
    stubbed = generate_stubs_for_unresolved(unresolved)
    log_results(sealed, installed, unresolved, stubbed)
    print(f"✅ Swarm sealed. Log saved to: {LOG}")

if __name__ == "__main__":
    main()