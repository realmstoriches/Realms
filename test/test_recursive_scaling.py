import json
import os

def find_packet(core, role):
    packet_dir = f"F:/Realms/{core}/agentic_launchpad/output/real_packets"
    print(f"🔍 Searching in: {packet_dir}")
    if not os.path.exists(packet_dir):
        print("❌ Packet directory not found.")
        return None
    for file in os.listdir(packet_dir):
        print(f"📦 Found file: {file}")
        if role in file:
            path = os.path.join(packet_dir, file)
            print(f"✅ Match found: {path}")
            return path
    print("❌ No matching packet found.")
    return None

BETA_PACKET = find_packet("realms_core_beta", "QAAnalyst")

def spawn_recursive_crew():
    if not BETA_PACKET or not os.path.exists(BETA_PACKET):
        print("❌ Packet file not found. Aborting.")
        return
    with open(BETA_PACKET, "r", encoding="utf-8") as f:
        packet = json.load(f)
    packet["recursive_spawn"] = {
        "crew_name": "Crew_Quality_RecursiveQA",
        "roles": ["QA Analyst", "Test Architect"],
        "spawned_by": "QA Analyst"
    }
    with open(BETA_PACKET, "w", encoding="utf-8") as f:
        json.dump(packet, f, indent=4)
    print("🧬 Recursive crew spawned in Beta.")

spawn_recursive_crew()