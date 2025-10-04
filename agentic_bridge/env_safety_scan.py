import os, sys, subprocess, importlib.util, logging
from datetime import datetime

LOG_PATH = r"F:\Realms\logs\env_safety_report.txt"
REQUIRED_MODULES = [
    "flask", "apscheduler", "chromadb", "tkinter", "ast", "json", "subprocess", "datetime"
]

logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

def log(msg):
    print(msg)
    logging.info(f"{datetime.now()} - {msg}")

def check_virtual_env():
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        log("✅ Virtual environment detected.")
    else:
        log("❌ Not running inside a virtual environment.")

def check_python_version():
    version = sys.version_info
    log(f"🧠 Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        log("⚠️ Python version may be outdated for some packages.")

def check_modules():
    missing = []
    for mod in REQUIRED_MODULES:
        if importlib.util.find_spec(mod) is None:
            missing.append(mod)
    if missing:
        log(f"❌ Missing modules: {missing}")
    else:
        log("✅ All required modules are available.")

def check_pip_integrity():
    try:
        result = subprocess.run(["python", "-m", "pip", "check"], capture_output=True, text=True)
        if result.returncode == 0:
            log("✅ pip check passed. No broken dependencies.")
        else:
            log("⚠️ pip check reported issues:")
            log(result.stdout.strip())
    except Exception as e:
        log(f"❌ pip check failed: {e}")

def scan_distutils_precedence():
    pth = os.path.join(sys.prefix, "lib", "site-packages", "distutils-precedence.pth")
    if os.path.exists(pth):
        try:
            with open(pth, "r") as f:
                line = f.readline().strip()
            if "add_shim" in line:
                log("⚠️ distutils-precedence.pth contains deprecated shim logic.")
            else:
                log("✅ distutils-precedence.pth appears clean.")
        except Exception as e:
            log(f"❌ Error reading distutils-precedence.pth: {e}")
    else:
        log("✅ distutils-precedence.pth not found. No shim issues.")

def run():
    log("🔍 Starting environment safety scan...")
    check_virtual_env()
    check_python_version()
    check_modules()
    check_pip_integrity()
    scan_distutils_precedence()
    log("✅ Scan complete. Review log for details.")

if __name__ == "__main__":
    run()