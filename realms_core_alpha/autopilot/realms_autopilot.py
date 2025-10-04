import sys, os, subprocess, threading, time, traceback, shutil, requests
from realms_dispatch_unified import dispatch_to_platform
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# 🔧 Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
BASE = Path("F:/Realms/realms_core_alpha")
ENV = BASE / ".env"
load_dotenv(dotenv_path=ENV, override=True)

# ✅ Proxy pool
def fetch_free_proxies():
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=1000&country=US&ssl=all&anonymity=elite"
    try:
        r = requests.get(url, timeout=5)
        proxies = r.text.strip().split("\n")
        return [p.strip() for p in proxies if p.strip()]
    except:
        return []

def validate_proxy(proxy_ip):
    proxy = {"http": f"http://{proxy_ip}", "https": f"http://{proxy_ip}"}
    try:
        r = requests.get("https://httpbin.org/ip", proxies=proxy, timeout=5)
        return r.status_code == 200
    except:
        return False

def get_valid_proxy():
    pool = fetch_free_proxies()
    for proxy_ip in pool:
        if validate_proxy(proxy_ip):
            print(f"✅ Proxy validated: {proxy_ip}")
            return {"http": f"http://{proxy_ip}", "https": f"http://{proxy_ip}"}
    print("❌ No valid proxies found.")
    return None

PROXIES = get_valid_proxy()

# 🔑 Stripe
import stripe
stripe.api_key = os.getenv("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# 🧠 Core agents
from realms_agentic_core.lead_harvest_agent import harvest_leads
from realms_agentic_core.email_validation_agent import validate_email_list
from superimage.content_creator import ContentCreator
from agentic_launchpad.modules.stripe_checkout_agent import inject_stripe_cta
from agentic_launchpad.make_payload_builder import build_payload
from agentic_launchpad.modules.email_campaign.email_dispatch_agent import dispatch_email_campaign
from agentic_launchpad.modules.syndication_agent import syndicate_to_channels
from realms_agentic_core.make_dispatch_trigger import trigger_make_scenario
from realms_agentic_core.dispatch_healer_agent import heal_dispatch_failures
from agentic_launchpad.system_healer import heal_system_if_needed
from realms_agentic_core.monetization.generate_revenue_chart import estimate_revenue
from agentic_launchpad.audit.fallback_manager import assign_fallback_agent
from agentic_launchpad.patch_and_repair import execute_repair
from agentic_launchpad.modules.email_campaign.thank_you_agent import send_thank_you_email
from agentic_launchpad.modules.upsell_agent import generate_upsell_payload
from realms_agentic_core.diagnostics.reflex_dispatcher import diagnose_failure

# 🌍 Constants
WEBSITE_URL = "https://www.realmstoriches.xyz"
STRIPE_CTA = "https://buy.stripe.com/test_4gwcN3g5g0gYfWc3cc"

# 🧠 FastAPI dashboard
app = FastAPI()
dashboard_data = []

@app.get("/dashboard", response_class=HTMLResponse)
def show_dashboard():
    html = "<h1>Realms Dispatch Dashboard</h1><table border='1'><tr><th>Cycle</th><th>Status</th><th>Emails</th><th>Revenue</th><th>Time</th><th>Notes</th></tr>"
    for entry in dashboard_data[-12:]:
        html += f"<tr><td>{entry['cycle_id']}</td><td>{entry['status']}</td><td>{entry['emails_sent']}</td><td>${entry['estimated_revenue']}</td><td>{entry['timestamp']}</td><td>{entry['notes']}</td></tr>"
        html += f"<tr><td colspan='6'><strong>Payload:</strong><div style='border:1px solid #ccc;padding:10px;background:#f9f9f9;'>{entry['payload_preview']}</div></td></tr>"
    html += "</table>"
    return html

@app.post("/manual-dispatch")
async def manual_dispatch(request: Request):
    data = await request.json()
    platform = data.get("platform")
    payload = data.get("payload")
    try:
        dispatch_to_platform(platform, payload, proxies=PROXIES)
        return {"status": "success", "message": f"Dispatched to {platform}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        return HTMLResponse(status_code=400, content="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        amount = session.get("amount_total", 0) / 100
        email = session.get("customer_email", "unknown")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        upsell = generate_upsell_payload(email)
        send_thank_you_email(email, upsell)

        dashboard_data.append({
            "cycle_id": f"STRIPE-{session['id']}",
            "status": "LIVE REVENUE",
            "emails_sent": 0,
            "estimated_revenue": amount,
            "timestamp": timestamp,
            "notes": f"Stripe checkout completed by {email}",
            "payload_preview": f"<strong>Upsell:</strong><br>{upsell.replace(chr(10), '<br>')}"
        })
        print(f"💰 Stripe payment received: ${amount} from {email}")
    return HTMLResponse(status_code=200, content="Webhook received")

def handle_failure(cycle_id, error):
    diagnosis = diagnose_failure(error)
    agent = assign_fallback_agent(diagnosis)
    execute_repair(agent, diagnosis)
    heal_dispatch_failures()
    heal_system_if_needed()
    try:
        print("🔁 Retrying after repair...")
        run_autopilot_cycle(cycle_id + "-RETRY")
    except Exception as retry_error:
        dashboard_data.append({
            "cycle_id": cycle_id,
            "status": "FAILURE",
            "emails_sent": 0,
            "estimated_revenue": 0,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "notes": f"Retry failed: {retry_error}",
            "payload_preview": "<em>No payload generated.</em>"
        })

def run_autopilot_cycle(cycle_id):
    try:
        domains = [
            "https://github.com/torvalds",
            "https://angel.co/companies",
            "https://www.crunchbase.com/discover",
            "https://www.producthunt.com/startups",
            "https://www.startupblink.com/startups/united-states"
        ]
        raw_emails = harvest_leads(domains)
        valid_emails = validate_email_list(raw_emails)
        if not valid_emails:
            raise ValueError("No valid emails found.")

        creator = ContentCreator()
        image_path = creator.generate_image(body="Activate your swarm")
        video_path = creator.generate_video(image_path)
        image_url = creator.upload(image_path)
        video_url = creator.upload(video_path)

        content = build_payload(image_url)
        content = inject_stripe_cta(content, STRIPE_CTA)
        content = inject_website_link(content, WEBSITE_URL)

        dispatch_email_campaign(valid_emails, content, image_url, video_url)
        syndicate_to_channels(image_path, content)
        trigger_make_scenario(content)

        revenue_estimate = estimate_revenue(len(valid_emails), content)

        dashboard_data.append({
            "cycle_id": cycle_id,
            "status": "SUCCESS",
            "emails_sent": len(valid_emails),
            "estimated_revenue": revenue_estimate,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "notes": "Autopilot cycle completed successfully.",
            "payload_preview": f"<strong>Content:</strong><br>{content.replace(chr(10), '<br>')}"
        })
        print(f"✅ Cycle {cycle_id} completed. Emails sent: {len(valid_emails)} | Estimated Revenue: ${revenue_estimate}")

    except Exception as e:
        print(f"❌ Cycle {cycle_id} failed: {e}")
        handle_failure(cycle_id, e)

if __name__ == "__main__":
    threading.Thread(
        target=lambda: subprocess.call([sys.executable, "-m", "uvicorn", "realms_autopilot:app", "--host", "0.0.0.0", "--port", "8000"]),
        daemon=True
    ).start()

    cycle_id = datetime.now().strftime("REALMS-%Y%m%d-%H%M%S")
    print(f"\n🧠 Launching cycle: {cycle_id}")
    run_autopilot_cycle(cycle_id)

    while True:
        time.sleep(5)    