import os
from pathlib import Path
import traceback

BASE = Path(__file__).resolve().parent
SUPERIMAGE = BASE.parent / "superimage"
PROMPTS = BASE.parent / "agentic_prompts"
INIT_FILES = [BASE, SUPERIMAGE, PROMPTS]

def safe_read(path):
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"⚠️ Unicode error in {path.name}. Retrying with fallback...")
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"❌ Failed to read {path.name}: {e}")
            return None

def safe_write(path, content):
    try:
        path.write_text(content, encoding="utf-8")
        print(f"✅ Patched: {path.name}")
    except Exception as e:
        print(f"❌ Failed to write {path.name}: {e}")

def heal_env_file():
    env_path = BASE.parent / ".env"
    if not env_path.exists():
        print("⚠️ .env not found. Creating...")
        env_path.write_text("", encoding="utf-8")
        return
    lines = safe_read(env_path).splitlines()
    clean = []
    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            key, val = line.strip().split("=", 1)
            val = val.strip()
            # Preserve quotes if value contains special characters
            if any(c in val for c in ['#', '*', ' ', '(', ')']):
                val = '"' + val.strip().strip('"').strip("'") + '"'
            clean.append(f"{key.strip()}={val}\n")
        else:
            clean.append(line + "\n")


    safe_write(env_path, "".join(clean))
    print("✅ .env healed")

def patch_config_manager():
    path = BASE / "config_manager.py"
    if not path.exists(): return
    code = safe_read(path)
    if code and "def get_env" not in code:
        patch = "\n\ndef get_env(var_name, default=None):\n    import os\n    return os.getenv(var_name, default)\n"
        safe_write(path, code + patch)

def patch_syndication_master():
    path = BASE / "syndication_master.py"
    if not path.exists(): return
    code = safe_read(path)
    if code and "superimage" in code:
        patch = (
            "import sys\nfrom pathlib import Path\n"
            "sys.path.append(str(Path(__file__).resolve().parent.parent / 'superimage'))\n"
        )
        updated = patch + code.replace("from superimage.", "from ")
        safe_write(path, updated)

def patch_realms_autopilot():
    path = BASE / "realms_autopilot.py"
    if not path.exists(): return
    code = safe_read(path)
    if code and "agentic_launchpad" in code:
        patch = (
            "import sys\nfrom pathlib import Path\n"
            "sys.path.append(str(Path(__file__).resolve().parent))\n"
        )
        updated = patch + code.replace("from agentic_launchpad.", "from ")
        safe_write(path, updated)

def patch_fallback_email():
    path = BASE / "fallback_email.py"
    if not path.exists(): return
    code = safe_read(path)
    if code and "realms_agentic_core.dispatch.dispatch_email" in code:
        patch = (
            "import sys\nfrom pathlib import Path\n"
            "sys.path.append(str(Path(__file__).resolve().parent.parent))\n"
        )
        updated = patch + code.replace(
            "from realms_agentic_core.dispatch.dispatch_email",
            "from dispatch.dispatch_email"
        )
        safe_write(path, updated)

def create_fallback_trigger():
    path = BASE / "fallback_trigger.py"
    if path.exists(): return
    fallback_code = """import subprocess
from pathlib import Path
BASE = Path(__file__).resolve().parent
REPAIR_CHAIN = ['syndication_master.py', 'realms_autopilot.py']
def run_repair(script_name):
    print(f'\\n🔧 Repairing: {script_name}')
    try:
        subprocess.run(['python', str(BASE / script_name)], check=True)
        print(f'✅ Recovered: {script_name}')
    except subprocess.CalledProcessError as e:
        print(f'❌ Repair failed: {script_name} → {e}')
def check_and_trigger():
    print('\\n🛡️ [fallback_trigger] Activating fallback recovery agents...')
    for script in REPAIR_CHAIN:
        run_repair(script)
    print('✅ Fallback recovery complete.')
"""
    safe_write(path, fallback_code)

def add_init_files():
    for folder in INIT_FILES:
        init_path = folder / "__init__.py"
        if not init_path.exists():
            safe_write(init_path, "")

def run_all_patches():
    print("\n🧠 Starting patch and repair sequence...")
    try:
        heal_env_file()
        patch_config_manager()
        patch_syndication_master()
        patch_realms_autopilot()
        patch_fallback_email()
        create_fallback_trigger()
        add_init_files()
        print("\n✅ All patches applied. System ready for launch.")
    except Exception:
        print("\n❌ Patch script failed unexpectedly:")
        traceback.print_exc()

def execute_repair():
    print("\n🛠️ [execute_repair] Running full patch and repair sequence...")
    run_all_patches()

if __name__ == "__main__":
    run_all_patches()