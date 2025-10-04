import schedule, time, subprocess, os

BASE_DIR = os.path.dirname(__file__)
def run_all():
    subprocess.run(["python", os.path.join(BASE_DIR, "email_scout.py")])
    subprocess.run(["python", os.path.join(BASE_DIR, "email_verifier.py")])
    subprocess.run(["python", os.path.join(BASE_DIR, "content_fetcher.py")])
    subprocess.run(["python", os.path.join(BASE_DIR, "campaign_sender.py")])

schedule.every().day.at("09:00").do(run_all)
schedule.every().day.at("12:00").do(run_all)
schedule.every().day.at("15:00").do(run_all)
schedule.every().day.at("18:00").do(run_all)
schedule.every().day.at("21:00").do(run_all)

print("🕒 CampaignScheduler: Running 5x daily.")
while True:
    schedule.run_pending()
    time.sleep(60)