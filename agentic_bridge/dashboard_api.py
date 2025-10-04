from flask import Flask, jsonify
import json

app = Flask(__name__)
DASHBOARD = r"F:\Realms\agentic_dashboard.json"

@app.route("/agents")
def agents():
    with open(DASHBOARD, "r") as f:
        data = json.load(f)
    return jsonify(data["agents"])

@app.route("/monetization")
def monetization():
    with open(DASHBOARD, "r") as f:
        data = json.load(f)
    return jsonify(data["monetization"])

@app.route("/syndication")
def syndication():
    with open(DASHBOARD, "r") as f:
        data = json.load(f)
    return jsonify(data["syndication"])

if __name__ == "__main__":
    app.run(port=5050)