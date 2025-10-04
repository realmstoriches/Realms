from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)
BRIDGE = r"F:\Realms\agentic_bridge"
SECRET = "realms_token_2025"

@app.route("/secure-trigger", methods=["POST"])
def secure_trigger():
    data = request.get_json()
    token = data.get("token")
    script = data.get("script")
    if token != SECRET:
        return jsonify({"error": "Unauthorized"}), 403
    try:
        subprocess.Popen(["python", f"{BRIDGE}\\{script}"])
        return jsonify({"status": f"{script} triggered"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8085)