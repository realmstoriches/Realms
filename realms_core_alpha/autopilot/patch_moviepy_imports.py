import os
from pathlib import Path

REALMS_ROOT = Path("F:/Realms")
LOG_FILE = REALMS_ROOT / "logs" / "moviepy_patch_log.txt"
LOG_FILE.parent.mkdir(exist_ok=True)

def patch_moviepy_imports():
    patched_files = []

    for file in REALMS_ROOT.rglob("*.py"):
        try:
            code = file.read_text(encoding="utf-8")
        except Exception:
            continue

        if "from moviepy import" in code:
            new_code = code.replace("from moviepy import", "from moviepy import")
            file.write_text(new_code, encoding="utf-8")
            patched_files.append(str(file))
            print(f"🔧 Patched: {file}")

    # Log results
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        log.write("✅ MoviePy import patch complete\n")
        log.write(f"Total files patched: {len(patched_files)}\n\n")
        for path in patched_files:
            log.write(f"{path}\n")

    print(f"\n✅ Patch complete. {len(patched_files)} files updated.")
    print(f"📄 Log saved to: {LOG_FILE}")

if __name__ == "__main__":
    patch_moviepy_imports()

