import json
import os
from src.agent import Agent
from src.company import ORG_CHART, generate_employee_file
from src.knowledge import KnowledgeBase
from src.tasks import generate_marketing_content, post_in_parallel, design_marketing_campaign
from src.ingestion import parse_product_data, ingest_text_file
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
    # --- Phase 1: Setup & Ingestion ---
    print("--- Phase 1: Setup & Ingestion ---")
    scrape_website_content("https://www.realmstoriches.xyz", "knowledge/brand_voice.txt")
    parse_product_data("data/raw_products.txt", "products/")

    marketing_kb = KnowledgeBase(collection_name="marketing_kb")
    ingest_text_file(marketing_kb, "knowledge/Marketing.txt")
    ingest_text_file(marketing_kb, "knowledge/brand_voice.txt")
    print("Knowledge bases populated.\n")

    # --- Phase 2: Assemble the Full Marketing Crew ---
    print("--- Phase 2: Assembling the Full Marketing Crew ---")
    strategist = create_agent_by_role("Campaign Strategist", marketing_kb)
    content_creator = create_agent_by_role("Marketing Content Creator", marketing_kb)
    social_manager = create_agent_by_role("Social Media Manager", KnowledgeBase(collection_name="social_kb"))
    print(f"Campaign Strategist '{strategist.name}' is on duty.")
    print(f"Content Creator '{content_creator.name}' is on duty.")
    print(f"Social Media Manager '{social_manager.name}' is on duty.\n")

    # --- Phase 3: The "Wow Feature" - Autonomous Campaign Execution ---
    print("--- Phase 3: Autonomous Campaign Execution ---")
    sample_product_filename = "products/american-walnut-limited-edition.json"
    if os.path.exists(sample_product_filename):
        with open(sample_product_filename, 'r') as f:
            product_data = json.load(f)

        print(f"Strategist is designing a campaign for: {product_data['product_name']}...")
        campaign = design_marketing_campaign(strategist, product_data)
        print("Campaign design complete.")
        print("--- CAMPAIGN PLAN ---")
        print(campaign['campaign_plan'])
        print("---------------------\n")

        print("Content Creator is generating posts based on the campaign...")
        generated_content = generate_marketing_content(content_creator, product_data)
        print("Content generation complete.\n")

        print("Social Media Manager is posting the content...")
        posting_results = post_in_parallel(
            content_dict={
                "twitter": generated_content["tweet"],
                "facebook": generated_content["facebook_post"],
                "linkedin": generated_content["facebook_post"],
                "wordpress": generated_content["facebook_post"],
                "instagram": generated_content["tweet"],
                "reddit": generated_content["facebook_post"]
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

    print("\n--- Full Workflow Complete ---")