import subprocess

BRIDGE = r"F:\Realms\agentic_bridge"
CYCLE = [
    "realms_orchestrator.py",
    "agentic_watchdog.py",
    "dispatch_supervisor.py",
    "revenue_tracker.py",
    "credential_rotator.py",
    "env_validator.py",
    "dashboard_api.py",
    "swarm_scheduler.py",
    "swarm_webhook.py",
    "swarm_daemon.py"
]

def run_cycle():
    print("🚀 Launching first full swarm cycle...")
    for script in CYCLE:
        subprocess.Popen(["python", f"{BRIDGE}\\{script}"])
    print("✅ All modules triggered.")

if __name__ == "__main__":
    run_cycle()