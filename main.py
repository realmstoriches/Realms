import json
from src.agent import Agent
from src.company import ORG_CHART, generate_employee_file
from src.ingestion import ingest_text_file
from src.knowledge import KnowledgeBase
from src.arrangements import ARRANGEMENT_TEMPLATES, generate_manifest
from src.testing import evaluate_product

def create_workforce(knowledge_base: KnowledgeBase):
    """
    Creates a workforce of agents based on the company's organizational chart,
    with all agents sharing a single knowledge base.
    """
    workforce = []
    for department, roles in ORG_CHART.items():
        for role_def in roles:
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
            workforce.append(agent)
    return workforce

if __name__ == "__main__":
    # --- Knowledge Ingestion ---
    shared_knowledge_base = KnowledgeBase(collection_name="workforce_kb")
    unique_departments = set(role['department'] for roles in ORG_CHART.values() for role in roles)
    print("Ingesting knowledge...")
    for department in unique_departments:
        knowledge_file = f"knowledge/{department}.txt"
        ingest_text_file(shared_knowledge_base, knowledge_file)

    # --- Arrangement Manifest Generation ---
    print("\n--- Generating Arrangement Manifest ---")
    development_template = ARRANGEMENT_TEMPLATES.get("Development")
    if development_template:
        generate_manifest("Development", development_template)

    # --- Product Testing Simulation ---
    print("\n--- Product Testing Simulation ---")
    with open("products/product_gemini.json", 'r') as f:
        product_to_test = json.load(f)
    print(f"Loaded product for evaluation: {product_to_test['product_name']}")

    testing_template = ARRANGEMENT_TEMPLATES.get("Testing Crew")
    if testing_template:
        testing_kb = KnowledgeBase(collection_name="testing_crew_kb")
        testing_crew_roster = [
            generate_employee_file(next(role for dept in ORG_CHART.values() for role in dept if role['title'] == title))
            for title in testing_template['roles']
        ]
        testing_crew = [
            Agent(
                name=agent_data['name'],
                role=agent_data['role_title'],
                employee_id=agent_data['employee_id'],
                hourly_rate=agent_data['hourly_rate'],
                physical_description=agent_data['physical_description'],
                skill_matrix=agent_data['skill_matrix'],
                knowledge_sources=agent_data['knowledge_sources'],
                tool_access=agent_data['tool_access'],
                knowledge_base=testing_kb
            ) for agent_data in testing_crew_roster
        ]
        print(f"Assembled a 'Testing Crew' with {len(testing_crew)} agents.")

        feedback = evaluate_product(testing_crew, product_to_test)

        print("\n--- Product Evaluation Feedback ---")
        for agent_name, response in feedback.items():
            print(f"Feedback from {agent_name} ({response['role']}):")
            print(f"  Question: {response['question']}")
            print(f"  Assessment: {response['assessment']}\n")
    else:
        print("Could not find the 'Testing Crew' arrangement template.")