import re
from pathlib import Path

# Files from diagnostic log
files_to_scan = [
    "realms_autopilot.py",
    "dispatch_wordpress.py",
    "dispatch_linkedin.py",
    "dispatch_email.py",
    "dispatch_facebook.py",
    "fallback_wordpress_dispatch.py",
    "fallback_linkedin.py",
    "fallback_email.py",
    "fallback_facebook.py",
    "fallback_fallback_email.py"
]

def scan_file(file_path):
    if not Path(file_path).exists():
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    dotenv_lines = [f"{file_path} [Line {i+1}]: {line.strip()}" for i, line in enumerate(lines) if "load_dotenv()" in line]
    commented_dispatch = [f"{file_path} [Line {i+1}]: {line.strip()}" for i, line in enumerate(lines) if line.strip().startswith("#") and ("dispatch" in line.lower() or "fallback" in line.lower())]
    return dotenv_lines, commented_dispatch

print("\n🔍 Rogue load_dotenv() calls:")
for file in files_to_scan:
    result = scan_file(file)
    if result:
        dotenv_lines, _ = result
        for line in dotenv_lines:
            print(line)

print("\n🧩 Commented dispatch/fallback lines:")
for file in files_to_scan:
    result = scan_file(file)
    if result:
        _, commented_lines = result
        for line in commented_lines:
            print(line)