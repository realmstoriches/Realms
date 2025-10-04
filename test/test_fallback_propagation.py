# Save in Realms/test/test_fallback_propagation.py
import json
import os

ALPHA_PACKET = "F:/Realms/realms_core_alpha/agentic_launchpad/output/real_packets/real_packet_Crew_Product_ProductLead.json"
BETA_PACKET = "F:/Realms/realms_core_beta/agentic_launchpad/output/real_packets/real_packet_Crew_Product_ProductLead.json"

def simulate_failure():
    with open(ALPHA_PACKET, "r", encoding="utf-8") as f:
        alpha = json.load(f)
    alpha["agents"] = []  # Simulate failure
    with open(ALPHA_PACKET, "w", encoding="utf-8") as f:
        json.dump(alpha, f, indent=4)
    print("❌ Alpha agent failed.")

def check_beta_fallback():
    with open(BETA_PACKET, "r", encoding="utf-8") as f:
        beta = json.load(f)
    fallback = beta.get("dispatch_logic", {}).get("fallback", [])
    print(f"✅ Beta fallback agents: {fallback}")

simulate_failure()
check_beta_fallback()