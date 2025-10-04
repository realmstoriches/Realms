from flask import Flask, jsonify, render_template_string
import json

app = Flask(__name__)
DASHBOARD = r"F:\Realms\agentic_dashboard.json"

@app.route("/")
def home():
    with open(DASHBOARD, "r") as f:
        data = json.load(f)
    html = (
        "<html><head><meta name='viewport' content='width=device-width'>"
        "<style>body{font-family:sans-serif;padding:10px;}table{width:100%;border-collapse:collapse;}td,th{border:1px solid #ccc;padding:8px;}</style></head><body>"
        "<h2>Agentic Dashboard</h2><table><tr><th>Name</th><th>Crew</th><th>Role</th><th>Status</th></tr>"
    )
    for agent in data["agents"]:
        html += f"<tr><td>{agent['name']}</td><td>{agent['crew']}</td><td>{agent['role']}</td><td>{agent['status']}</td></tr>"
    html += "</table></body></html>"
    return render_template_string(html)

@app.route("/api")
def api():
    with open(DASHBOARD, "r") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(port=5055)
