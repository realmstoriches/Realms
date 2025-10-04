import os, json, stripe
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from dotenv import dotenv_values
from pydantic import BaseModel
from uvicorn import run as uvicorn_run

BASE = Path(__file__).resolve().parent
ENV_PATH = BASE.parent / ".env"
DISPATCH_LOG = BASE / "dispatch_log.json"
EARNINGS_LOG = BASE / "earnings_log.json"

env = dotenv_values(ENV_PATH)
stripe.api_key = env.get("STRIPE_API_KEY")
stripe_cta = env.get("STRIPE_PAYMENT_LINK", "https://buy.stripe.com/test_abc123456")
website_link = env.get("BLOG_FRONTEND_URL", "https://www.realmstoriches.xyz")

app = FastAPI()
earnings_total = 0

class DispatchPayload(BaseModel):
    platform: str
    title: str
    body: str
    images: list[str]
    videos: list[str]
    links: list[str]

@app.get("/", response_class=HTMLResponse)
def dashboard():
    dispatches = []
    if DISPATCH_LOG.exists():
        dispatches = json.loads(DISPATCH_LOG.read_text(encoding="utf-8"))
    earnings = json.loads(EARNINGS_LOG.read_text(encoding="utf-8")) if EARNINGS_LOG.exists() else {}
    html = f"<h1>🧠 Realms Dashboard</h1><p>Total Earnings: ${earnings.get('daily_estimate', 0):.2f}</p><hr>"
    for d in dispatches[-10:]:
        html += f"<h3>{d['title']}</h3><p>{d['body']}</p><p>Images: {len(d['images'])}, Videos: {len(d['videos'])}</p><p>Links: {', '.join(d['links'])}</p><hr>"
    return html

@app.post("/dispatch/")
def receive_dispatch(payload: DispatchPayload):
    validated = stripe_cta in payload.body and website_link in payload.body
    log = {
        "platform": payload.platform,
        "title": payload.title,
        "body": payload.body,
        "images": payload.images,
        "videos": payload.videos,
        "links": payload.links,
        "cta_validated": validated
    }
    logs = []
    if DISPATCH_LOG.exists():
        logs = json.loads(DISPATCH_LOG.read_text(encoding="utf-8"))
    logs.append(log)
    DISPATCH_LOG.write_text(json.dumps(logs, indent=2), encoding="utf-8")
    return {"status": "✅ Dispatch received", "cta_validated": validated}

@app.post("/webhook/")
async def stripe_webhook(request: Request):
    payload = await request.body()
    event = json.loads(payload)
    if event["type"] == "checkout.session.completed":
        amount = event["data"]["object"]["amount_total"]
        global earnings_total
        earnings_total += amount / 100
        EARNINGS_LOG.write_text(json.dumps({"daily_estimate": earnings_total}, indent=2), encoding="utf-8")
        return {"status": "💰 Stripe payment received"}
    return {"status": "ignored"}

def launch_dashboard():
    print("🚀 Launching Realms Dashboard on http://localhost:8000")
    uvicorn_run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    launch_dashboard()
