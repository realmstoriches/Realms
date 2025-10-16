from src.agent import Agent
from src.company import ORG_CHART, generate_employee_file
from src.ingestion import ingest_text_file
from src.knowledge import KnowledgeBase

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
                knowledge_base=knowledge_base  # Inject the shared KB
            )
            workforce.append(agent)
    return workforce

if __name__ == "__main__":
    # Create a single, shared knowledge base for the entire workforce
    shared_knowledge_base = KnowledgeBase(collection_name="workforce_kb")

    # Ingest knowledge for each department only once
    unique_departments = set(role['department'] for roles in ORG_CHART.values() for role in roles)
    print("Ingesting knowledge...")
    for department in unique_departments:
        knowledge_file = f"knowledge/{department}.txt"
        ingest_text_file(shared_knowledge_base, knowledge_file)

    # Create the workforce
    workforce = create_workforce(shared_knowledge_base)
    print(f"\nCreated a workforce with {len(workforce)} agents.")

    # Example: Have a software agent process a problem
    software_agent = next((agent for agent in workforce if agent.role == "Graphics Driver Engineer"), None)
    if software_agent:
        problem = "What is important for collaboration?"
        decision = software_agent.process(problem)

        print(f"\nAgent {software_agent.name} ({software_agent.role}) is processing the problem: '{problem}'")
        print(f"Final Decision: {decision}")
        print(f"Decision Log: {software_agent.decision_logs[-1]}")
    else:
        print("\nCould not find a 'Graphics Driver Engineer' to run the example.")