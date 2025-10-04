# reflex_dispatcher.py
import time, subprocess

AGENTIC_TASKS = [
    {"name": "WordPress Dispatch", "cmd": "python dispatch_wordpress.py"},
    {"name": "LinkedIn Syndication", "cmd": "python dispatch_linkedin.py"},
    {"name": "Fallback Email", "cmd": "python fallback_email.py"}
]

def run_task(task):
    try:
        subprocess.run(task["cmd"], shell=True, check=True)
    except subprocess.CalledProcessError:
        log_failure(task["name"])
        reroute(task)

def log_failure(name):
    with open("reflex_log.txt", "a") as f:
        f.write(f"{time.ctime()} - FAILED: {name}\n")

def reroute(task):
    fallback = f"python fallback_{task['name'].lower().replace(' ', '_')}.py"
    subprocess.run(fallback, shell=True)

for task in AGENTIC_TASKS:
    run_task(task)