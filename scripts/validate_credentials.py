import os
import sys
from dotenv import dotenv_values

# Add the project root to the Python path to allow for `src` imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import all authentication functions
from src.social import twitter, facebook, linkedin, wordpress, instagram, reddit

import argparse

def validate_credentials(env_path):
    """
    Reads required keys from .env.example, checks them against the specified
    .env file, and attempts to authenticate with each service.
    """
    print("--- Starting Credential Validation ---")

    # 1. Read required keys from .env.example
    try:
        with open(".env.example", "r") as f:
            required_keys = [line.split('=')[0] for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print("Error: .env.example not found. Cannot determine required credentials.")
        return

    # 2. Check for the .env file
    if not os.path.exists(env_path):
        print(f"Error: Environment file not found at '{env_path}'.")
        print("Please run `python scripts/setup_credentials.py` first.")
        return

    # 3. Load the user's credentials
    user_creds = dotenv_values(env_path)

    # 4. Check for missing or empty keys
    missing_keys = [key for key in required_keys if key not in user_creds or not user_creds[key]]

    if missing_keys:
        print("\n--- Missing Credentials ---")
        print("The following required credentials are missing or empty in your .env file:")
        for key in missing_keys:
            print(f" - {key}")
        print("\nPlease run `python scripts/setup_credentials.py` to set them.")

    print("\n--- Attempting Authentication ---")
    # A mapping of keys to their respective authentication functions
    auth_map = {
        "TWITTER_API_KEY": twitter.authenticate,
        "FACEBOOK_APP_ID": facebook.authenticate,
        "LINKEDIN_CLIENT_ID": linkedin.authenticate,
        "WORDPRESS_USER": wordpress.authenticate,
        "INSTAGRAM_USERNAME": instagram.authenticate,
        "REDDIT_CLIENT_ID": reddit.authenticate,
    }

    # Load the .env file for the auth functions to use
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)

    for key, auth_func in auth_map.items():
        if key in user_creds and user_creds[key]:
            print(f"Validating credentials for {key.split('_')[0]}...")
            auth_func()
        else:
            print(f"Skipping validation for {key.split('_')[0]} (credentials not provided).")

    print("\n--- Validation Complete ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate social media credentials.")
    parser.add_argument(
        '--env_file',
        type=str,
        default='.env',
        help='Path to the .env file to validate.'
    )
    args = parser.parse_args()

    validate_credentials(args.env_file)