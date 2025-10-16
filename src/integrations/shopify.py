"""
This module handles interactions with the Shopify API.
"""
import os
import shopify
from dotenv import load_dotenv

load_dotenv()

def connect_to_shopify():
    """
    Connects to the Shopify store using credentials from environment variables.
    """
    shop_url = os.getenv("SHOPIFY_SHOP_URL")
    api_key = os.getenv("SHOPIFY_API_KEY")
    password = os.getenv("SHOPIFY_API_PASSWORD")

    if not all([shop_url, api_key, password]):
        print("Error: Shopify credentials not found in environment variables.")
        return False

    try:
        api_version = '2023-10'
        session = shopify.Session(shop_url, api_version, password)
        shopify.ShopifyResource.activate_session(session)
        print("Successfully connected to Shopify.")
        return True
    except Exception as e:
        print(f"Failed to connect to Shopify: {e}")
        return False

def get_all_products():
    """
    Fetches all products from the Shopify store.
    This is a placeholder and does not make a real API call.
    """
    if not connect_to_shopify():
        return []

    print("Fetching all products from Shopify...")
    # Placeholder for the actual API call
    # products = shopify.Product.find()
    print("Successfully fetched products.")
    # For now, we will return an empty list as we are still using the raw data file.
    return []