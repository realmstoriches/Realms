import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required = [
    "requests",
    "beautifulsoup4",
    "dnspython",
    "python-dotenv"
]

for pkg in required:
    try:
        install(pkg)
        print(f"✅ Installed: {pkg}")
    except Exception as e:
        print(f"❌ Failed to install {pkg}: {e}")