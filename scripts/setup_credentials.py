"""
An interactive script to securely set up API credentials in a .env file.
"""
import os

def setup_credentials():
    """
    Prompts the user for API credentials and saves them to a .env file.
    """
    print("--- Social Media Credential Setup ---")
    print("Please enter your API credentials. Press Enter to skip any you don't have.")

    credentials = {
        "TWITTER_API_KEY": input("Enter your Twitter API Key: "),
        "TWITTER_API_SECRET": input("Enter your Twitter API Secret: "),
        "FACEBOOK_APP_ID": input("Enter your Facebook App ID: "),
        "FACEBOOK_APP_SECRET": input("Enter your Facebook App Secret: "),
        "LINKEDIN_CLIENT_ID": input("Enter your LinkedIn Client ID: "),
        "LINKEDIN_CLIENT_SECRET": input("Enter your LinkedIn Client Secret: "),
        "WORDPRESS_USER": input("Enter your WordPress Username: "),
        "WORDPRESS_PASSWORD": input("Enter your WordPress Application Password: "),
        "INSTAGRAM_USERNAME": input("Enter your Instagram Username: "),
        "INSTAGRAM_PASSWORD": input("Enter your Instagram Password: "),
        "REDDIT_CLIENT_ID": input("Enter your Reddit Client ID: "),
        "REDDIT_CLIENT_SECRET": input("Enter your Reddit Client Secret: "),
        "REDDIT_USERNAME": input("Enter your Reddit Username: "),
        "REDDIT_PASSWORD": input("Enter your Reddit Password: "),
    }

    # Filter out any empty values
    final_credentials = {k: v for k, v in credentials.items() if v}

    with open(".env", "w") as f:
        for key, value in final_credentials.items():
            f.write(f"{key}=\"{value}\"\n")

    print("\nCredentials have been saved to the .env file.")
    print("This file is ignored by git and will not be committed.")

if __name__ == "__main__":
    setup_credentials()