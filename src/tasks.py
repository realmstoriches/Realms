"""
This module contains logic for orchestrating various agent tasks,
such as product testing and content generation.
"""
import concurrent.futures
from typing import List, Dict
from src.agent import Agent
from src.social import twitter, facebook, linkedin, wordpress, instagram, reddit

# A registry of available social media platforms
SOCIAL_PLATFORMS = {
    "twitter": twitter.post_update,
    "facebook": facebook.post_update,
    "linkedin": linkedin.post_update,
    "wordpress": wordpress.post_update,
    "instagram": instagram.post_update,
    "reddit": reddit.post_update,
}

def post_in_parallel(content_dict: Dict[str, str], product_name: str, subreddits: List[str] = None):
    """
    Posts content to all social media platforms in parallel.

    Args:
        content_dict (Dict[str, str]): A dictionary where keys are platform
                                       names and values are the content to post.
    """
    results = []
    subreddits = subreddits or ["yourproductsubreddit"] # Default subreddit

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_platform = {}
        for platform, content in content_dict.items():
            if platform in SOCIAL_PLATFORMS:
                if platform == "wordpress":
                    future = executor.submit(SOCIAL_PLATFORMS[platform], content, title=f"Introducing: {product_name}")
                    future_to_platform[future] = platform
                elif platform == "instagram":
                    future = executor.submit(SOCIAL_PLATFORMS[platform], content, image_path=f"products/images/{product_name}.jpg")
                    future_to_platform[future] = platform
                elif platform == "reddit":
                    for sub in subreddits:
                        future = executor.submit(SOCIAL_PLATFORMS[platform], content, subreddit=sub, title=f"Check out our new {product_name}!")
                        future_to_platform[future] = f"{platform} (r/{sub})"
                else:
                    future = executor.submit(SOCIAL_PLATFORMS[platform], content)
                    future_to_platform[future] = platform

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
    variants = product_data.get("variants", [])

    # Create a more detailed prompt with product specifics
    features = []
    if variants:
        # Just grab the first variant's options as representative features
        first_variant_options = variants[0].get("options", {})
        features = [f"{k}: {v}" for k, v in first_variant_options.items()]

    features_str = ", ".join(features)

    # Create a more detailed prompt
    prompt_details = f"Product: {product_name}. Key features: {features_str}."

    # Generate a tweet
    tweet_prompt = f"Create a short, exciting tweet for the following product. {prompt_details}"
    tweet = agent.process(tweet_prompt)

    # Generate a Facebook post
    facebook_prompt = f"Write an engaging Facebook post for the following product, highlighting its benefits. {prompt_details}"
    facebook_post = agent.process(facebook_prompt)

    return {
        "tweet": tweet,
        "facebook_post": facebook_post
    }

def design_marketing_campaign(agent: Agent, product_data: dict):
    """
    Assigns a Campaign Strategist to design a marketing campaign for a product.
    """
    product_name = product_data.get("product_name", "our product")

    prompt = (
        f"Design a comprehensive, multi-platform marketing campaign for the launch of '{product_name}'. "
        f"Include target audience analysis, key messaging pillars, and a suggested timeline for "
        f"Twitter, Facebook, and a WordPress blog announcement."
    )

    campaign_plan = agent.process(prompt)

    return {
        "product_name": product_name,
        "campaign_plan": campaign_plan
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