"""
This module contains logic for orchestrating various agent tasks,
such as product testing and content generation.
"""
import concurrent.futures
from typing import List, Dict
from src.agent import Agent
from src.social import twitter, facebook

# A registry of available social media platforms
SOCIAL_PLATFORMS = {
    "twitter": twitter.post_update,
    "facebook": facebook.post_update,
}

def post_in_parallel(content_dict: Dict[str, str]):
    """
    Posts content to all social media platforms in parallel.

    Args:
        content_dict (Dict[str, str]): A dictionary where keys are platform
                                       names and values are the content to post.
    """
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_platform = {
            executor.submit(SOCIAL_PLATFORMS[platform], content): platform
            for platform, content in content_dict.items()
            if platform in SOCIAL_PLATFORMS
        }
        for future in concurrent.futures.as_completed(future_to_platform):
            platform = future_to_platform[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"'{platform}' generated an exception: {exc}")
    return results

def generate_marketing_content(agent: Agent, product_data: dict):
    """
    Assigns a marketing agent to generate social media content for a product.
    """
    product_name = product_data.get("product_name", "our latest product")

    # Simulate generating a tweet
    tweet_prompt = f"Create a short, punchy tweet for {product_name}."
    tweet = agent.process(tweet_prompt)

    # Simulate generating a Facebook post
    facebook_prompt = f"Write an engaging Facebook post for {product_name}, highlighting its key features."
    facebook_post = agent.process(facebook_prompt)

    return {
        "tweet": tweet,
        "facebook_post": facebook_post
    }

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