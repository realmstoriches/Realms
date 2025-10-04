import subprocess
import os

BASE = "realms_core_alpha/agentic_launchpad/modules/email_campaign"

print("🔗 Starting chained email campaign...\n")

steps = [
    ("📡 EmailScout", "email_scout.py"),
    ("✅ EmailVerifier", "email_verifier.py"),
    ("📝 ContentFetcher", "content_fetcher.py"),
    ("📤 CampaignSender", "campaign_sender.py")
]

for label, script in steps:
    print(f"{label}: Running {script}")
    subprocess.run(["python", os.path.join(BASE, script)])

print("\n✅ Email campaign completed.")