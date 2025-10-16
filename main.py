import json
import os
from src.agent import Agent
from src.company import ORG_CHART, generate_employee_file
from src.knowledge import KnowledgeBase
from src.tasks import generate_marketing_content, post_in_parallel
from src.ingestion import ingest_text_file
from scripts.parse_products import parse_product_data

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
    # Parse the raw product data into structured JSON files
    parse_product_data("data/raw_products.txt", "products/")

    # Create and populate the knowledge base for the marketing agent
    marketing_kb = KnowledgeBase(collection_name="marketing_kb")
    ingest_text_file(marketing_kb, "knowledge/Marketing.txt")
    print("Marketing knowledge base populated.\n")

    # --- Phase 2: Assemble the Crew ---
    print("--- Phase 2: Assembling the Crew ---")
    marketing_agent = create_agent_by_role("Marketing Content Creator", marketing_kb)
    social_media_manager = create_agent_by_role("Social Media Manager", KnowledgeBase(collection_name="social_kb"))
    print(f"Marketing Agent '{marketing_agent.name}' is on duty.")
    print(f"Social Media Manager '{social_media_manager.name}' is on duty.\n")

    # --- Phase 3: Content Generation and Posting ---
    print("--- Phase 3: Content Generation and Posting for 5 Sample Products ---")
    product_files = [f for f in os.listdir("products") if f.endswith('.json')]

    for i, product_file in enumerate(product_files[:5]): # Process first 5 products
        print(f"\n--- Processing Product {i+1}: {product_file} ---")
        product_path = os.path.join("products", product_file)

        with open(product_path, 'r') as f:
            product_data = json.load(f)

        # a. Generate content
        print(f"Generating content for: {product_data['product_name']}...")
        generated_content = generate_marketing_content(marketing_agent, product_data)
        print("Content generation complete.")
        print(f"  Tweet: {generated_content['tweet']}")
        print(f"  Facebook Post: {generated_content['facebook_post']}")


        # b. Post content in parallel
        print("\nAssigning Social Media Manager to post content...")
        posting_results = post_in_parallel({
            "twitter": generated_content["tweet"],
            "facebook": generated_content["facebook_post"]
        })

        print("Posting complete.")
        for result in posting_results:
            if result:
                print(f"  -> Successfully posted to {result['platform']}.")
            else:
                print("  -> A post failed.")

    print("\n--- Workflow Complete ---")