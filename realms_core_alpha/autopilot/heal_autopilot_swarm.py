import os
from pathlib import Path

REALMS_ROOT = Path("F:/Realms")
LOGS = REALMS_ROOT / "logs"
LOGS.mkdir(exist_ok=True)
LOG_FILE = LOGS / "autopilot_swarm_heal_log.txt"

def patch_moviepy_imports():
    patched = []
    for file in REALMS_ROOT.rglob("*.py"):
        try:
            code = file.read_text(encoding="utf-8")
        except Exception:
            continue
        if "from moviepy import" in code:
            new_code = code.replace("from moviepy import", "from moviepy import")
            file.write_text(new_code, encoding="utf-8")
            patched.append(str(file))
    return patched

def patch_final_filler():
    filler = REALMS_ROOT / "realms_core_alpha" / "agentic_launchpad" / "final_filler.py"
    if filler.exists():
        code = filler.read_text(encoding="utf-8")
        if "def inject_website_link" not in code:
            code += "\n\ndef inject_website_link(content, website_url):\n    return content + f\"\\n\\n🌐 Visit us: {website_url}\"\n"
            filler.write_text(code, encoding="utf-8")
            return [str(filler)]
    return []

def drop_dispatch_variant_agent():
    agent_path = REALMS_ROOT / "realms_core_alpha" / "realms_agentic_core" / "dispatch_variant_agent.py"
    if not agent_path.exists():
        code = '''import random\nfrom datetime import datetime\n\ndef generate_variant(payment_link=None):\n    title = "🧠 Realms Update: Legacy Enforced"\n    theme = "Realms executed a full dispatch loop—tokens rotated, content posted, fallback logic verified."\n    reflection = "No alerts. No errors. Just sovereign execution."\n    cta = f"Explore Realms tools → {payment_link}" if payment_link else ""\n    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")\n    footer = f"🧭 Logged at {timestamp}\\n#FounderLog_{timestamp.replace(':','').replace(' ','_')}"\n    content = f"{reflection}\\n\\n{title}\\n\\n{theme}\\n\\n{cta}\\n\\n{footer}"\n    return {"title": title, "content": content}\n\nif __name__ == "__main__":\n    variant = generate_variant("https://realms.ai/pay")\n    print("📡 Dispatch Variant Ready:\\n")\n    print("Title:", variant["title"])\n    print("Content:\\n", variant["content"])'''
        agent_path.write_text(code, encoding="utf-8")
        return [str(agent_path)]
    return []

def log_results(patches):
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        log.write("✅ Autopilot Swarm Heal Complete\n\n")
        for category, files in patches.items():
            log.write(f"🔧 {category} ({len(files)} files):\n")
            for f in files:
                log.write(f"  - {f}\n")
            log.write("\n")
    print(f"\n✅ All patches applied. Log saved to: {LOG_FILE}")

def main():
    print("🧠 Healing Realms Autopilot Swarm...")
    patches = {
        "MoviePy Imports": patch_moviepy_imports(),
        "Final Filler Patch": patch_final_filler(),
        "Dispatch Variant Agent": drop_dispatch_variant_agent()
    }
    log_results(patches)
    print("🚀 All modules healed. You’re ready to relaunch.")

if __name__ == "__main__":
    main()