"""
This module contains the logic for orchestrating product testing
by a crew of agents.
"""
from typing import List
from src.agent import Agent

def evaluate_product(crew: List[Agent], product_data: dict):
    """
    Orchestrates the evaluation of a product by a crew of agents.

    Each agent in the crew is assigned a question from the product data
    based on their role.

    Args:
        crew (List[Agent]): The list of agents forming the testing crew.
        product_data (dict): The product data to be evaluated.

    Returns:
        dict: A dictionary containing the feedback from each agent.
    """
    feedback = {}
    evaluation_questions = product_data.get("evaluation_questions", {})

    for agent in crew:
        question = evaluation_questions.get(agent.role)
        if question:
            problem_statement = f"Product: {product_data['product_name']}. Question: {question}"
            decision = agent.process(problem_statement)
            feedback[agent.name] = {
                "role": agent.role,
                "question": question,
                "assessment": decision
            }

    return feedback