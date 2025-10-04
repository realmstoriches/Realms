import re
from pathlib import Path

AUTOPILOT = Path("F:/Realms/realms_core_alpha/autopilot/realms_autopilot.py")
DISPATCH_DIR = Path("F:/Realms/realms_core_alpha/realms_agentic_core/dispatch")
FALLBACK_DIR = Path("F:/Realms/realms_core_alpha/realms_agentic_core/fallback")
LOG = Path("F:/Realms/logs/autopilot_refactor_log.txt")
LOG.parent.mkdir(exist_ok=True)

def ensure_init(path):
    for folder in [path, path.parent]:
        init = folder / "__init__.py"
        if not init.exists():
            init.write_text("", encoding="utf-8")

def refactor_autopilot():
    if not AUTOPILOT.exists():
        print("❌ realms_autopilot.py not found.")
        return

    code = AUTOPILOT.read_text(encoding="utf-8")
    lines = code.splitlines()
    new_lines = []
    import_lines = set()
    missing_agents = []

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

            if agent_path.exists():
                ensure_init(agent_path.parent)
                import_lines.add(f"from {module} import {agent}")
                new_lines.append(f"{agent}()")
            else:
                missing_agents.append(str(agent_path))
                new_lines.append(f"# ❌ Missing agent: {agent}.py")
        else:
            new_lines.append(line)

    header = "\n".join(sorted(import_lines))
    patched = header + "\n\n" + "\n".join(new_lines)
    AUTOPILOT.write_text(patched, encoding="utf-8")

    with open(LOG, "w", encoding="utf-8") as f:
        f.write("✅ Autopilot Refactor Complete\n\n")
        f.write("🔧 Imports Injected:\n")
        for imp in sorted(import_lines):
            f.write(f"{imp}\n")
        f.write("\n❌ Missing Agents:\n")
        for miss in missing_agents:
            f.write(f"{miss}\n")

    print(f"✅ Refactor complete. Imports injected. Missing agents logged to: {LOG}")

if __name__ == "__main__":
    refactor_autopilot()