import os
import shutil
import json

ROOT_DIR = os.path.abspath("F:/realms_core/agentic_launchpad")
DATA_DIR = os.path.join(ROOT_DIR, "data")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
PACKET_DIR = os.path.join(OUTPUT_DIR, "real_packets")

REQUIRED_DATA_FILES = [
    "agents.json", "crews.json", "fallbacks.json", "personas.json", "domains.json"
]

def ensure_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(PACKET_DIR, exist_ok=True)

def find_file(filename):
    for root, _, files in os.walk(ROOT_DIR):
        if filename in files:
            return os.path.join(root, filename)
    return None

def move_file(src, dest_folder):
    dest = os.path.join(dest_folder, os.path.basename(src))
    if os.path.abspath(src) != os.path.abspath(dest):
        shutil.move(src, dest)
        print(f"🔁 Moved {os.path.basename(src)} → {dest_folder}")

def heal_data_files():
    for filename in REQUIRED_DATA_FILES:
        expected_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(expected_path):
            found = find_file(filename)
            if found:
                move_file(found, DATA_DIR)
            else:
                print(f"❌ Missing file: {filename}")

def heal_packet_files():
    for root, _, files in os.walk(ROOT_DIR):
        for file in files:
            if file.startswith("real_packet_") and file.endswith(".json"):
                current_path = os.path.join(root, file)
                if os.path.abspath(os.path.dirname(current_path)) != os.path.abspath(PACKET_DIR):
                    move_file(current_path, PACKET_DIR)

def run_healer():
    print("🧠 Running Realms System Healer...")
    ensure_directories()
    heal_data_files()
    heal_packet_files()
    print("✅ System healing complete. All files are in their proper locations.")

if __name__ == "__main__":
    run_healer()