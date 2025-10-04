import tkinter as tk
import subprocess

BRIDGE = r"F:\Realms\agentic_bridge"
MODULES = {
    "Orchestrator": "realms_orchestrator.py",
    "Dispatch": "dispatch_supervisor.py",
    "Watchdog": "agentic_watchdog.py",
    "Revenue": "revenue_tracker.py",
    "Rotate Credentials": "credential_rotator.py",
    "Validate .env": "env_validator.py",
    "Dashboard API": "dashboard_api.py",
    "Webhook Server": "swarm_webhook.py",
    "Scheduler": "swarm_scheduler.py"
}

def launch(script):
    subprocess.Popen(["python", f"{BRIDGE}\\{script}"])

root = tk.Tk()
root.title("🧭 Sovereign Swarm GUI")
for name, script in MODULES.items():
    tk.Button(root, text=name, width=30, command=lambda s=script: launch(s)).pack(pady=4)

root.mainloop()