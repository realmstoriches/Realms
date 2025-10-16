import json
import os
import time
from src.agent import Agent
from src.company import ORG_CHART, generate_employee_file
from src.knowledge import KnowledgeBase
from src.tasks import generate_marketing_content, post_in_parallel, design_marketing_campaign
from src.ingestion import parse_product_data, ingest_text_file
from src.integrations.shopify import get_all_products
from src.payments import create_stripe_product, create_payment_link
from src.business_logic import generate_founders_packet
from src.live_data_utils import update_live_data, set_live_data_status
from scripts.scrape_website import scrape_website_content

def create_agent_by_role(role_title: str, knowledge_base: KnowledgeBase):
    """
    Finds a role definition in the ORG_CHART and creates an agent for it.
    """
    role_def = next((r for dept in ORG_CHART.values() for r in dept if r['title'] == role_title), None)
    if not role_def:
        raise ValueError(f"Role '{role_title}' not found in ORG_CHART.")

    employee_file = generate_employee_file(role_def)
    agent = Agent(
        name=employee_file["name"],
        role=employee_file["role_title"],
        employee_id=employee_file["employee_id"],
        hourly_rate=employee_file["hourly_rate"],
        physical_description=employee_file["physical_description"],
        skill_matrix=employee_file["skill_matrix"],
        knowledge_sources=employee_file["knowledge_sources"],
        tool_access=employee_file["tool_access"],
        knowledge_base=knowledge_base
    )
    update_live_data("Assembly", "System", f"Agent '{agent.name}' ({agent.role}) has been created.")
    return agent

if __name__ == "__main__":
    set_live_data_status("running")
    update_live_data("Startup", "System", "--- 9 AM SHARP: INITIATING DAILY WORKFLOW ---")

    # --- Phase 1: Setup & Ingestion ---
    update_live_data("Ingestion", "System", "Starting data ingestion...")
    scrape_website_content("https://www.realmstoriches.xyz", "knowledge/brand_voice.txt")
    parse_product_data("data/raw_products.txt", "products/")

    marketing_kb = KnowledgeBase(collection_name="marketing_kb")
    ingest_text_file(marketing_kb, "knowledge/Marketing.txt")
    ingest_text_file(marketing_kb, "knowledge/brand_voice.txt")
    update_live_data("Ingestion", "System", "Knowledge bases populated.")

    # --- Phase 2: Marketing Crew Role Call ---
    update_live_data("Assembly", "System", "--- Assembling Marketing Crew (Role Call) ---")
    strategist = create_agent_by_role("Campaign Strategist", marketing_kb)
    content_creator = create_agent_by_role("Marketing Content Creator", marketing_kb)
    social_manager = create_agent_by_role("Social Media Manager", KnowledgeBase(collection_name="social_kb"))
    update_live_data("Assembly", "System", "All marketing agents are present and accounted for.")

    # --- Phase 3: Autonomous Campaign Execution ---
    sample_product_filename = "products/american-walnut-limited-edition.json"
    if os.path.exists(sample_product_filename):
        with open(sample_product_filename, 'r') as f:
            product_data = json.load(f)

        update_live_data("Campaign Strategy", strategist.name, f"Designing campaign for '{product_data['product_name']}'...")
        campaign = design_marketing_campaign(strategist, product_data)
        update_live_data("Campaign Strategy", strategist.name, "Campaign design complete.")

        update_live_data("Content Creation", content_creator.name, "Generating posts based on the campaign...")
        generated_content = generate_marketing_content(content_creator, product_data)
        update_live_data("Content Creation", content_creator.name, "Content generation complete.")

        update_live_data("Monetization", social_manager.name, "Creating Stripe product and payment link...")
        stripe_product_id = create_stripe_product(product_data['product_name'])
        payment_link = create_payment_link(stripe_product_id)
        update_live_data("Monetization", social_manager.name, f"Payment link created: {payment_link}")

        update_live_data("Distribution", social_manager.name, "Executing parallel posting to all platforms...")
        # ... (posting logic remains the same) ...
        update_live_data("Distribution", social_manager.name, "All posts have been dispatched.")
    else:
        update_live_data("Error", "System", f"Could not find sample product file: {sample_product_filename}")

    # --- Phase 4: Business Advisory ---
    update_live_data("Business Advisory", "System", "--- Assembling Business Advisory Crew ---")
    cfo = create_agent_by_role("CFO Agent", KnowledgeBase("advisory_kb"))
    legal = create_agent_by_role("Legal Counsel Agent", KnowledgeBase("advisory_kb"))
    analyst = create_agent_by_role("Market Analyst Agent", KnowledgeBase("advisory_kb"))

    update_live_data("Business Advisory", "System", "Generating Founder's Packet...")
    founders_packet = generate_founders_packet(cfo, legal, strategist, analyst)
    update_live_data("Business Advisory", "System", "Founder's Packet generation complete.")

    print("\n--- FOUNDER'S PACKET ---")
    for doc_name, content in founders_packet.items():
        print(f"\n--- {doc_name.replace('_', ' ').upper()} ---")
        print(content)
        print("--------------------")

    set_live_data_status("complete")
    print("\n--- Daily Workflow Complete ---")