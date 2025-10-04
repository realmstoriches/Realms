import requests
import json

SCENARIOS = {
    "WordPress": "https://hook.make.com/your-wordpress-id",
    "LinkedIn": "https://hook.make.com/your-linkedin-id"
}

def check_status():
    status = {}
    for name, url in SCENARIOS.items():
        try:
            r = requests.get(url, timeout=5)
            status[name] = "Online" if r.status_code == 200 else f"Error {r.status_code}"
        except Exception as e:
            status[name] = f"Exception: {str(e)}"

    with open("logs/syndication_status.json", "w") as f:
        json.dump(status, f, indent=2)

    print("✅ Syndication status saved to logs/syndication_status.json")

if __name__ == "__main__":
    check_status()