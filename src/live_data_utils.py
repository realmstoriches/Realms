import json
import os
from datetime import datetime

LIVE_DATA_FILE = "live_data.json"
MAX_LOG_ENTRIES = 50

def update_live_data(phase, event_agent, event_action):
    """
    Updates the shared live_data.json file with the current status and a new event.
    """
    # Ensure the file exists with a default structure
    if not os.path.exists(LIVE_DATA_FILE):
        data = {"status": "initialized", "last_update": None, "current_phase": "Idle", "recent_events": []}
    else:
        try:
            with open(LIVE_DATA_FILE, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            data = {"status": "error", "last_update": None, "current_phase": "Error", "recent_events": []}

    # Update the main status fields
    data["status"] = "running"
    data["current_phase"] = phase
    data["last_update"] = datetime.now().isoformat()

    # Add the new event
    new_event = {
        "timestamp": data["last_update"],
        "agent": event_agent,
        "action": event_action
    }
    data["recent_events"].append(new_event)

    # Keep the log from growing indefinitely
    if len(data["recent_events"]) > MAX_LOG_ENTRIES:
        data["recent_events"] = data["recent_events"][-MAX_LOG_ENTRIES:]

    # Write the updated data back to the file
    with open(LIVE_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def set_live_data_status(status: str):
    """Sets the final status of the live data file."""
    try:
        with open(LIVE_DATA_FILE, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data = {"status": "initialized", "last_update": None, "current_phase": "Idle", "recent_events": []}

    data["status"] = status
    data["last_update"] = datetime.now().isoformat()
    with open(LIVE_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)