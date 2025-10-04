import re
from pathlib import Path

AUTOPILOT_PATH = Path("F:/Realms/realms_core_alpha/autopilot/realms_autopilot.py")
DISPATCH_ROOT = "realms_agentic_core.dispatch"
FALLBACK_ROOT = "realms_agentic_core.fallback"

def refactor_autopilot():
    if not AUTOPILOT_PATH.exists():
        print("❌ realms_autopilot.py not found.")
        return

    code = AUTOPILOT_PATH.read_text(encoding="utf-8")
    lines = code.splitlines()
    new_lines = []
    import_lines = set()

    for line in lines:
        match = re.search(r'os\.system\(["\']python ([\w_]+)\.py["\']\)', line.strip())
        if match:
            script_name = match.group(1)
            if "fallback" in script_name:
                module_path = f"{FALLBACK_ROOT}.{script_name}"
            else:
                module_path = f"{DISPATCH_ROOT}.{script_name}"
            import_lines.add(f"from {module_path} import {script_name}")
            new_lines.append(f"{script_name}()")
        else:
            new_lines.append(line)

    # Inject imports at the top
    header = "\n".join(sorted(import_lines))
    patched_code = header + "\n\n" + "\n".join(new_lines)
    AUTOPILOT_PATH.write_text(patched_code, encoding="utf-8")

    print(f"✅ Refactored os.system calls in: {AUTOPILOT_PATH.name}")
    print(f"📦 Imports injected for: {', '.join(sorted(import_lines))}")

if __name__ == "__main__":
    refactor_autopilot()