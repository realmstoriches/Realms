import json
import os
import shutil

ALPHA_DIR = os.path.abspath("Realms/realms_core_alpha/agentic_launchpad")
BETA_DIR = os.path.abspath("Realms/realms_core_beta/agentic_launchpad")

def sync_packets():
    alpha_packets = os.path.join(ALPHA_DIR, "output", "real_packets")
    beta_packets = os.path.join(BETA_DIR, "output", "real_packets")
    os.makedirs(beta_packets, exist_ok=True)

    for file in os.listdir(alpha_packets):
        if file.startswith("real_packet_") and file.endswith(".json"):
            src = os.path.join(alpha_packets, file)
            dst = os.path.join(beta_packets, file)
            shutil.copy2(src, dst)
            print(f"🔁 Synced {file} → Beta")

def sync_confirmation_chains():
    alpha_data = os.path.join(ALPHA_DIR, "data", "agents.json")
    beta_data = os.path.join(BETA_DIR, "data", "agents.json")

    with open(alpha_data, "r", encoding="utf-8") as f:
        alpha_agents = json.load(f)
    with open(beta_data, "r", encoding="utf-8") as f:
        beta_agents = json.load(f)

    alpha_roles = {a["role_title"]: a["name"] for a in alpha_agents}
    beta_roles = {a["role_title"]: a["name"] for a in beta_agents}

    shared_roles = set(alpha_roles.keys()) & set(beta_roles.keys())
    confirmation_chain = sorted(list({alpha_roles[r] for r in shared_roles if r in ["Strategic PM", "Systems Architect", "Product Lead"]}))

    for packet_dir in [os.path.join(ALPHA_DIR, "output", "real_packets"), os.path.join(BETA_DIR, "output", "real_packets")]:
        for file in os.listdir(packet_dir):
            if file.startswith("real_packet_") and file.endswith(".json"):
                path = os.path.join(packet_dir, file)
                with open(path, "r", encoding="utf-8") as f:
                    packet = json.load(f)
                packet["confirmation_chain"] = confirmation_chain
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(packet, f, indent=4)
                print(f"🔐 Injected confirmation chain into {file}")

def run_bridge():
    print("🧠 Running Pantheon Bridge...")
    sync_packets()
    sync_confirmation_chains()
    print("✅ Twin sync complete. Alpha and Beta are now mirrored.")

if __name__ == "__main__":
    run_bridge()