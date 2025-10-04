from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/status")
def status():
    return jsonify({
        "Realms": "Live",
        "Monetization": "Active",
        "Crews": "Scheduled",
        "Fallback": "Enabled",
        "Recursive": "Operational"
    })

if __name__ == "__main__":
    app.run(port=5051)