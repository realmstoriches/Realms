import os
import re
from pathlib import Path

ROOT = Path("F:/Realms/realms_core_alpha")
AUTOPILOT = ROOT / "autopilot" / "realms_autopilot.py"
DISPATCH_DIR = ROOT / "realms_agentic_core" / "dispatch"
FALLBACK_DIR = ROOT / "realms_agentic_core" / "fallback"
LOG = ROOT / "logs" / "swarm_validation_log.txt"
LOG.parent.mkdir(exist_ok=True)

def ensure_init(path):
    sealed = []
    for folder in [path, path.parent]:
        init = folder / "__init__.py"
        if not init.exists():
            init.write_text("", encoding="utf-8")
            sealed.append(str(init))
    return sealed

def generate_stub(path, func_name):
    stub = f"def {func_name}():\n    print(\"🧪 Stub agent {func_name} activated\")\n"
    path.write_text(stub, encoding="utf-8")
    return str(path)

def scan_autopilot_for_shell_calls():
    shell_calls = []
    if not AUTOPILOT.exists():
        return shell_calls
    code = AUTOPILOT.read_text(encoding="utf-8")
    for match in re.findall(r'os\.system\(["\']python ([\w_]+)\.py["\']\)', code):
        shell_calls.append(match)
    return shell_calls

def refactor_autopilot(shell_calls):
    if not AUTOPILOT.exists():
        return [], []
    code = AUTOPILOT.read_text(encoding="utf-8")
    lines = code.splitlines()
    new_lines = []
    import_lines = set()
    stubbed = []

    for line in lines:
        match = re.search(r'os\.system\(["\']python ([\w_]+)\.py["\']\)', line.strip())
        if match:
            agent = match.group(1)
            if "fallback" in agent:
                agent_path = FALLBACK_DIR / f"{agent}.py"
                module = f"realms_agentic_core.fallback.{agent}"
            else:
                agent_path = DISPATCH_DIR / f"{agent}.py"
                module = f"realms_agentic_core.dispatch.{agent}"

            ensure_init(agent_path.parent)
            if not agent_path.exists():
                stubbed.append(generate_stub(agent_path, agent))
            import_lines.add(f"from {module} import {agent}")
            new_lines.append(f"{agent}()")
        else:
            new_lines.append(line)

    header = "\n".join(sorted(import_lines))
    patched = header + "\n\n" + "\n".join(new_lines)
    AUTOPILOT.write_text(patched, encoding="utf-8")
    return sorted(import_lines), stubbed

def scan_for_missing_imports():
    missing = []
    for file in ROOT.rglob("*.py"):
        try:
            code = file.read_text(encoding="utf-8")
        except Exception:
            continue
        for match in re.findall(r'from ([\w\.]+) import ([\w_]+)', code):
            module_path = ROOT / Path(match[0].replace(".", "/") + ".py")
            if not module_path.exists():
                missing.append((file.name, match[0], match[1]))
    return missing

def seal_all_modules():
    sealed = []
    for folder in ROOT.rglob("*"):
        if folder.is_dir() and "modules" in folder.parts:
            sealed += ensure_init(folder)
    return sealed

def log_results(imports, stubs, missing_imports, sealed_inits):
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("✅ Final Swarm Validation Report\n\n")
        f.write("🔧 Imports Injected:\n")
        for imp in imports:
            f.write(f"{imp}\n")
        f.write("\n🧪 Stub Agents Generated:\n")
        for stub in stubs:
            f.write(f"{stub}\n")
        f.write("\n❌ Missing Imports:\n")
        for file, module, symbol in missing_imports:
            f.write(f"{file}: from {module} import {symbol} → NOT FOUND\n")
        f.write("\n🧱 __init__.py Injected:\n")
        for path in sealed_inits:
            f.write(f"{path}\n")

def main():
    print("🧠 Healing and validating swarm...")
    shell_calls = scan_autopilot_for_shell_calls()
    imports, stubs = refactor_autopilot(shell_calls)
    missing_imports = scan_for_missing_imports()
    sealed_inits = seal_all_modules()
    log_results(imports, stubs, missing_imports, sealed_inits)
    print(f"✅ Swarm sealed. Log saved to: {LOG}")

if __name__ == "__main__":
    main()