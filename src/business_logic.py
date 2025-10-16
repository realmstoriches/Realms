"""
This module contains tasks for the Business Advisory crew to generate
strategic documents and financial projections.
"""
from src.agent import Agent

def generate_financial_projections(cfo_agent: Agent):
    """
    Has the CFO Agent generate financial projections.
    """
    prompt = "Generate a 3-year financial projection, including revenue forecasts, cost of goods sold, and net income. Assume a 50% year-over-year growth rate."
    projections = cfo_agent.process(prompt)
    return projections

def generate_legal_agreement(legal_agent: Agent):
    """
    Has the Legal Counsel Agent generate a standard Founders' Agreement template.
    """
    prompt = "Draft a simple Founders' Agreement template. Include clauses for equity distribution, roles and responsibilities, vesting, and intellectual property assignment."
    agreement = legal_agent.process(prompt)
    return agreement

def generate_pitch_deck_outline(strategist_agent: Agent):
    """
    Has the Campaign Strategist generate a pitch deck outline.
    """
    prompt = "Create a 10-slide pitch deck outline. Include slides for the problem, solution, market size, product, business model, team, and financial projections."
    outline = strategist_agent.process(prompt)
    return outline

def generate_audience_profiles(analyst_agent: Agent):
    """
    Has the Market Analyst Agent generate target audience profiles.
    """
    prompt = "Create two detailed target audience personas. Include demographics, psychographics, goals, and pain points. Also, create one anti-persona of a customer we should not target."
    profiles = analyst_agent.process(prompt)
    return profiles

def generate_founders_packet(cfo, legal, strategist, analyst):
    """
    Orchestrates the generation of the complete Founder's Packet.
    """
    print("[CFO] Generating financial projections...")
    projections = generate_financial_projections(cfo)

    print("[LEGAL] Drafting Founders' Agreement...")
    agreement = generate_legal_agreement(legal)

    print("[STRATEGIST] Outlining pitch deck...")
    pitch_deck = generate_pitch_deck_outline(strategist)

    print("[ANALYST] Developing audience profiles...")
    audience = generate_audience_profiles(analyst)

    return {
        "financial_projections": projections,
        "founders_agreement_template": agreement,
        "pitch_deck_outline": pitch_deck,
        "audience_profiles": audience,
    }