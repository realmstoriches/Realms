from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
PACKET_DIR = "F:/Realms/realms_core_alpha/agentic_launchpad/output/real_packets"

@app.route("/dispatch", methods=["POST"])
def dispatch():
    crew = request.json.get("crew")
    packet_path = os.path.join(PACKET_DIR, f"real_packet_{crew}.json")
    if not os.path.exists(packet_path):
        return jsonify({"error": "Packet not found"}), 404
    with open(packet_path, "r", encoding="utf-8") as f:
        packet = json.load(f)
    return jsonify(packet)

@app.route("/list_crews", methods=["GET"])
def list_crews():
    crews = [f.replace("real_packet_", "").replace(".json", "") for f in os.listdir(PACKET_DIR)]
    return jsonify({"crews": crews})

if __name__ == "__main__":
    app.run(port=5050)