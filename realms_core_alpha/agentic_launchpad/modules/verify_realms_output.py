import os
import json

BASE = "F:/Realms/realms_core_alpha/agentic_launchpad/modules"

def check_file(path, required_keys=None):
    full_path = os.path.join(BASE, path)
    if not os.path.exists(full_path):
        return f"❌ Missing: {path}"
    if required_keys:
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for key in required_keys:
                if key not in data:
                    return f"⚠️ {path} missing key: {key}"
        except Exception as e:
            return f"❌ Error reading {path}: {e}"
    return f"✅ Verified: {path}"

def run_checks():
    print("🔍 Verifying Realms Output...\n")

    checks = [
        check_file("dispatch_manifest.json", ["agents", "pricing", "business_plan"]),
        check_file("agent_manifest.json", ["new_agents"]),
        check_file("pricing_model.json", ["tiers", "per_mission"]),
        check_file("business_plan.json", ["mission", "objectives", "crew_assignments"]),
        check_file("../output/real_packets/real_packet_Crew_Design_UIDesigner.json", ["agents", "fallbacks", "dispatch_logic"]),
        check_file("../output/real_packets/real_packet_Crew_Quality_QAAnalyst.json", ["recursive_spawn"]),
    ]

    for result in checks:
        print(result)

    print("\n📦 Verification complete.")

if __name__ == "__main__":
    run_checks()