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
from scripts.scrape_website import scrape_website_content

def create_agent_by_role(role_title: str, knowledge_base: KnowledgeBase):
    """
    Finds a role definition in the ORG_CHART and creates an agent for it.
    """
    role_def = next((r for dept in ORG_CHART.values() for r in dept if r['title'] == role_title), None)
    if not role_def:
        raise ValueError(f"Role '{role_title}' not found in ORG_CHART.")

    employee_file = generate_employee_file(role_def)
    return Agent(
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

if __name__ == "__main__":
    print("--- 9 AM SHARP: INITIATING DAILY MARKETING & SALES WORKFLOW ---")

    # --- Phase 1: Setup & Ingestion ---
    print("\n--- Phase 1: Setup & Ingestion ---")
    scrape_website_content("https://www.realmstoriches.xyz", "knowledge/brand_voice.txt")

    # In a live environment, we would use the Shopify API.
    # For now, we continue to use the local file for consistency.
    # get_all_products()
    parse_product_data("data/raw_products.txt", "products/")

    marketing_kb = KnowledgeBase(collection_name="marketing_kb")
    ingest_text_file(marketing_kb, "knowledge/Marketing.txt")
    ingest_text_file(marketing_kb, "knowledge/brand_voice.txt")
    print("Knowledge bases populated.")

    # --- Phase 2: Marketing Crew Role Call ---
    print("\n--- Phase 2: Marketing Crew Role Call ---")
    strategist = create_agent_by_role("Campaign Strategist", marketing_kb)
    content_creator = create_agent_by_role("Marketing Content Creator", marketing_kb)
    social_manager = create_agent_by_role("Social Media Manager", KnowledgeBase(collection_name="social_kb"))

    print(f"  [PRESENT] Campaign Strategist: {strategist.name}")
    print(f"  [PRESENT] Content Creator: {content_creator.name}")
    print(f"  [PRESENT] Social Media Manager: {social_manager.name}")
    print("All marketing agents are present and accounted for.\n")

    # --- Phase 3: Autonomous Campaign Execution ---
    print("--- Phase 3: Autonomous Campaign Execution ---")
    sample_product_filename = "products/american-walnut-limited-edition.json"
    if os.path.exists(sample_product_filename):
        with open(sample_product_filename, 'r') as f:
            product_data = json.load(f)

        print(f"\n[STRATEGIST] {strategist.name}: Designing campaign for '{product_data['product_name']}'...")
        time.sleep(1)
        campaign = design_marketing_campaign(strategist, product_data)
        print("[STRATEGIST] Campaign design complete.")
        print("\n--- CAMPAIGN PLAN ---")
        print(campaign['campaign_plan'])
        print("---------------------\n")

        print(f"[CREATOR] {content_creator.name}: Generating posts based on the campaign...")
        time.sleep(1)
        generated_content = generate_marketing_content(content_creator, product_data)
        print("[CREATOR] Content generation complete.\n")

        print(f"[MANAGER] {social_manager.name}: Creating Stripe product and payment link...")
        time.sleep(1)
        stripe_product_id = create_stripe_product(product_data['product_name'])
        payment_link = create_payment_link(stripe_product_id)
        print(f"[MANAGER] Payment link created: {payment_link}\n")

        print(f"[MANAGER] {social_manager.name}: Executing parallel posting...")
        tweet_with_link = f"{generated_content['tweet']}\n\nBuy now: {payment_link}"
        facebook_post_with_link = f"{generated_content['facebook_post']}\n\nGet yours here: {payment_link}"
        posting_results = post_in_parallel(
            content_dict={
                "twitter": tweet_with_link,
                "facebook": facebook_post_with_link,
                "linkedin": facebook_post_with_link,
                "wordpress": facebook_post_with_link,
                "instagram": tweet_with_link,
                "reddit": facebook_post_with_link
            },
            product_name=product_data['product_name']
        )

        print("\n--- Posting Results ---")
        for result in posting_results:
            if result:
                print(f"  -> Post to {result.get('platform', 'N/A')} successful.")
            else:
                print("  -> A post failed.")
    else:
        print(f"Could not find sample product file: {sample_product_filename}")

    # --- Phase 4: Business Advisory Crew Generates Founder's Packet ---
    print("\n--- Phase 4: Business Advisory Crew Role Call ---")
    advisory_kb = KnowledgeBase(collection_name="advisory_kb") # Dedicated KB
    cfo = create_agent_by_role("CFO Agent", advisory_kb)
    legal = create_agent_by_role("Legal Counsel Agent", advisory_kb)
    analyst = create_agent_by_role("Market Analyst Agent", advisory_kb)

    print(f"  [PRESENT] CFO: {cfo.name}")
    print(f"  [PRESENT] Legal Counsel: {legal.name}")
    print(f"  [PRESENT] Market Analyst: {analyst.name}")
    print("All advisory agents are present and accounted for.\n")

    print("--- Generating Founder's Packet ---")
    founders_packet = generate_founders_packet(cfo, legal, strategist, analyst)
    print("\n--- FOUNDER'S PACKET ---")
    for doc_name, content in founders_packet.items():
        print(f"\n--- {doc_name.replace('_', ' ').upper()} ---")
        print(content)
        print("--------------------")

    print("\n--- Daily Workflow Complete ---")