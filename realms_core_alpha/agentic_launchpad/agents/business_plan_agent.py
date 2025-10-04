import json
from pathlib import Path

def generate_comprehensive_plan():
    base = Path(__file__).parent.parent
    with open(base / "business" / "business_plan.json") as f:
        plan = json.load(f)

    md = f"""# Comprehensive Business Plan

## Executive Summary
{plan['brand']} aims to {plan['mission']}

## Company Description
Vision: {plan['mission']}
Core Values: Autonomy, Resilience, Agentic Execution

## Market Analysis
Target Market: {', '.join(plan['content_strategy']['channels'])}
Themes: {', '.join(plan['content_strategy']['themes'])}

## Competitive Analysis
We differentiate through full agentic automation and sovereign infrastructure.

## Products and Services
Software that builds, monetizes, and prepares itself for IPO.

## Marketing and Sales Strategy
Automated syndication, email campaigns, and social outreach.

## Organizational Structure
Agents defined by HRMAgent based on this plan.

## Financial Projections
Monetization via {', '.join(plan['monetization']['methods'])}
Break-even expected within 12 months.
"""
    with open(base / "business" / "Comprehensive_Business_Plan.md", "w") as out:
        out.write(md)

if __name__ == "__main__":
    generate_comprehensive_plan()
