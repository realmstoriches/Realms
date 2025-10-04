import subprocess, time, os

BRIDGE = r"F:\Realms\agentic_bridge"
WATCHED = ["dashboard_api.py", "swarm_webhook.py", "swarm_scheduler.py"]

def is_running(script):
    return script in subprocess.getoutput("tasklist")

def restart(script):
    subprocess.Popen(["python", f"{BRIDGE}\\{script}"])
    print(f"🔁 Restarted {script}")

while True:
    for script in WATCHED:
        if not is_running(script):
            restart(script)
    time.sleep(60)