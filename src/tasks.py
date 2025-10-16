"""
This module contains logic for orchestrating various agent tasks,
such as product testing and content generation.
"""
import concurrent.futures
from typing import List, Dict
from src.agent import Agent
from src.social import twitter, facebook, linkedin, wordpress, instagram, reddit
from src.throttling import throttler
from src.logging import log_post_performance

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
                throttler.wait_if_needed(platform)
                if platform == "wordpress":
                    future = executor.submit(SOCIAL_PLATFORMS[platform], content, title=f"Introducing: {product_name}")
                    future_to_platform[future] = platform
                elif platform == "instagram":
                    future = executor.submit(SOCIAL_PLATFORMS[platform], content, image_path=f"products/images/{product_name}.jpg")
                    future_to_platform[future] = platform
                elif platform == "reddit":
                    for sub in subreddits:
                        throttler.wait_if_needed(platform) # Check for each subreddit post
                        future = executor.submit(SOCIAL_PLATFORMS[platform], content, subreddit=sub, title=f"Check out our new {product_name}!")
                        future_to_platform[future] = f"{platform} (r/{sub})"
                else:
                    future = executor.submit(SOCIAL_PLATFORMS[platform], content)
                    future_to_platform[future] = platform

        for future in concurrent.futures.as_completed(future_to_platform):
            platform = future_to_platform[future]
            try:
                result = future.result()
                if result and result.get('status') == 'success':
                    log_post_performance(product_name, platform, success=True)
                else:
                    log_post_performance(product_name, platform, success=False)
                results.append(result)
            except Exception as exc:
                print(f"'{platform}' generated an exception: {exc}")
                log_post_performance(product_name, platform, success=False)
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
    Includes a summary of past performance to allow for self-refinement.
    """
    product_name = product_data.get("product_name", "our product")

    # Read past performance to inform the new campaign
    performance_summary = ""
    try:
        with open("logs/social_media_performance.log", "r") as f:
            # Get the last 10 lines for a recent summary
            recent_performance = f.readlines()[-10:]
            if recent_performance:
                performance_summary = "Reviewing recent performance:\n" + "".join(recent_performance)
    except FileNotFoundError:
        pass # No past performance to review

    prompt = (
        f"{performance_summary}\n\n"
        f"Based on this, design a new, comprehensive marketing campaign for '{product_name}'. "
        f"Include target audience, key messaging, and a timeline for Twitter, Facebook, and a blog."
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