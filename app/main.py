from flask import Flask, jsonify, redirect, request
import json
import os

app = Flask(__name__)

# --- Live Data Endpoint ---
@app.route('/api/live_data')
def get_live_data():
    """
    Reads the live data from the shared JSON file and serves it.
    """
    # Construct the path to the root directory's live_data.json
    live_data_path = os.path.join(os.path.dirname(__file__), '..', 'live_data.json')
    try:
        with open(live_data_path, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"status": "waiting for data..."}), 404
    except json.JSONDecodeError:
        return jsonify({"status": "error reading data"}), 500

# --- Placeholder OAuth 2.0 Endpoints ---
@app.route('/auth/<platform>/login')
def oauth_login(platform):
    """
    Placeholder to start the OAuth flow. In a real app, this would
    redirect to the social media platform's authorization URL.
    """
    # In a real implementation, you would generate the state and redirect
    # return redirect(f"https://{platform}.com/oauth/authorize?client_id=...&scope=...")
    return f"This would redirect you to {platform} to authorize the application."

@app.route('/auth/<platform>/callback')
def oauth_callback(platform):
    """
    Placeholder for the OAuth callback. In a real app, this would
    handle the authorization code, exchange it for a token, and
    store the token securely.
    """
    auth_code = request.args.get('code')
    # In a real implementation, you would exchange the code for a token
    # and save it to your secure store.
    return f"Successfully received callback from {platform} with auth code: {auth_code}. You can now close this window."

if __name__ == '__main__':
    # Note: For development only. Use a production WSGI server (e.g., Gunicorn) in production.
    app.run(debug=True, port=5001)