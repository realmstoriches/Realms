import json
import os
from src.agent import Agent
from src.company import ORG_CHART, generate_employee_file
from src.knowledge import KnowledgeBase
from src.tasks import generate_marketing_content, post_in_parallel
from src.ingestion import ingest_text_file
from src.ingestion import ingest_text_file
from scripts.parse_products import parse_product_data
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
    # Scrape website for brand voice
    scrape_website_content("https://www.realmstoriches.xyz", "knowledge/brand_voice.txt")

    # Parse the raw product data into structured JSON files
    parse_product_data("data/raw_products.txt", "products/")

    # Create and populate the knowledge base for the marketing agent
    marketing_kb = KnowledgeBase(collection_name="marketing_kb")
    ingest_text_file(marketing_kb, "knowledge/Marketing.txt")
    ingest_text_file(marketing_kb, "knowledge/brand_voice.txt")
    print("Marketing knowledge base populated.\n")

    # --- Phase 2: Assemble the Crew ---
    print("--- Phase 2: Assembling the Crew ---")
    marketing_agent = create_agent_by_role("Marketing Content Creator", marketing_kb)
    social_media_manager = create_agent_by_role("Social Media Manager", KnowledgeBase(collection_name="social_kb"))
    print(f"Marketing Agent '{marketing_agent.name}' is on duty.")
    print(f"Social Media Manager '{social_media_manager.name}' is on duty.\n")

    # --- Phase 3: Content Generation and Posting ---
    print("--- Phase 3: Content Generation and Posting ---")
    sample_product_filename = "products/american-walnut-limited-edition.json"
    if os.path.exists(sample_product_filename):
        with open(sample_product_filename, 'r') as f:
            product_data = json.load(f)

        print(f"Generating content for product: {product_data['product_name']}...")
        generated_content = generate_marketing_content(marketing_agent, product_data)

        print("\nAssigning Social Media Manager to post content in parallel...")
        posting_results = post_in_parallel(
            content_dict={
                "twitter": generated_content["tweet"],
                "facebook": generated_content["facebook_post"],
                "linkedin": generated_content["facebook_post"], # Reuse for LinkedIn
                "wordpress": generated_content["facebook_post"], # Reuse for WordPress
                "instagram": generated_content["tweet"], # Shorter content for Instagram
                "reddit": generated_content["facebook_post"]
            },
            product_name=product_data['product_name'],
            subreddits=["product_announcements", "gadgets"]
        )

        print("\n--- Posting Results ---")
        for result in posting_results:
            if result:
                print(f"Successfully posted to {result.get('platform', 'N/A')}.")
            else:
                print("A post failed.")
    else:
        print(f"Could not find sample product file: {sample_product_filename}")

    print("\n--- Workflow Complete ---")