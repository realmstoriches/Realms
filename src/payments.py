"""
This module handles interactions with the Stripe API for payments.
"""
import os
import stripe
from dotenv import load_dotenv
import random

load_dotenv()

def create_stripe_product(product_name: str):
    """
    Creates a new product in Stripe.
    This is a placeholder and does not make a real API call.
    """
    stripe.api_key = os.getenv("STRIPE_API_KEY")
    if not stripe.api_key:
        print("Stripe API key not found. Skipping product creation.")
        return None

    print(f"Creating Stripe product for: {product_name}")
    product_id = f"prod_{random.randint(1000, 9999)}"
    print(f"Successfully created Stripe product with ID: {product_id}")
    return product_id

def create_payment_link(product_id: str, price_usd: float = 9.99):
    """
    Creates a new payment link for a given product ID.
    This is a placeholder and does not make a real API call.
    """
    stripe.api_key = os.getenv("STRIPE_API_KEY")
    if not stripe.api_key or not product_id:
        return None

    print(f"Creating Stripe payment link for product: {product_id}")
    payment_link_url = f"https://buy.stripe.com/placeholder_{random.randint(1000, 9999)}"
    print(f"Successfully created payment link: {payment_link_url}")
    return payment_link_url