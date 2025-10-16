"""
Provides information and signup links for the social media platforms
and tools used by the agent workforce.
"""

def get_tool_info():
    """
    Prints a list of required tools and their signup/developer links.
    """
    tools = {
        "Twitter": "https://developer.twitter.com/en/docs/authentication/oauth-2-0",
        "Facebook": "https://developers.facebook.com/docs/pages-api/",
        "LinkedIn": "https://www.linkedin.com/developers/apps/new",
        "WordPress": "https://wordpress.com/support/applications/application-passwords/",
        "Instagram": "https://developers.facebook.com/docs/instagram-basic-display-api",
        "Reddit": "https://www.reddit.com/prefs/apps",
        "Hootsuite": "https://www.hootsuite.com/plans/free-trial",
        "Canva": "https://www.canva.com/",
        "Buffer": "https://buffer.com/signup",
        "Sprout Social": "https://sproutsocial.com/signup/",
        "Salesforce": "https://www.salesforce.com/form/signup/freetrial-sales/",
        "Marketo": "https://www.marketo.com/free-trial/",
        "Asana": "https://asana.com/create-account",
    }

    print("--- Tool & Developer Account Signup Links ---")
    print("To enable all features of the agentic workforce, you will need developer accounts for the following platforms:")
    for tool, link in tools.items():
        print(f"- {tool}: {link}")
    print("\nNote: For some platforms, you may need to create a 'developer app' to get API keys.")

if __name__ == "__main__":
    get_tool_info()