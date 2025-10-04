import json
from pathlib import Path

BASE = Path(__file__).parent.parent
PLAN = BASE / "business" / "business_plan.json"
DECK = BASE / "business" / "investor_pitch_deck.md"

def generate_deck():
    with open(PLAN) as f:
        plan = json.load(f)
    md = f"""# Investor Pitch Deck

## Brand
{plan['brand']}

## Mission
{plan['mission']}

## Market Opportunity
Themes: {', '.join(plan['content_strategy']['themes'])}
Channels: {', '.join(plan['content_strategy']['channels'])}

## Product
Agentic automation platform for outreach, monetization, and legacy creation.

## Monetization
Methods: {', '.join(plan['monetization']['methods'])}
CTA: {plan['monetization']['cta']}

## Infrastructure
Blog: {plan['infrastructure']['blog_subdomain']}
Host: {plan['infrastructure']['host']}

## Automation
Platform: {plan['automation']['platform']}
Trigger: {plan['automation']['trigger']}
"""
    with open(DECK, "w") as f:
        f.write(md)
    print("📊 Investor pitch deck generated.")

if __name__ == "__main__":
    generate_deck()
