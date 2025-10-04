from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

BRIDGE = r"F:\Realms\agentic_bridge"

def run_script(name):
    subprocess.run(["python", f"{BRIDGE}\\{name}"])

sched = BlockingScheduler()

# Hourly health check
@sched.scheduled_job('interval', hours=1)
def hourly_watchdog():
    run_script("agentic_watchdog.py")

# Daily revenue tracking
@sched.scheduled_job('cron', hour=0)
def daily_revenue():
    run_script("revenue_tracker.py")

# Weekly credential rotation
@sched.scheduled_job('cron', day_of_week='sun', hour=3)
def weekly_rotation():
    run_script("credential_rotator.py")

# Daily dispatch
@sched.scheduled_job('cron', hour=9)
def daily_dispatch():
    run_script("dispatch_supervisor.py")

if __name__ == "__main__":
    print("🕒 Swarm Scheduler running...")
    sched.start()