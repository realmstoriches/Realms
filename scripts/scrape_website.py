"""
This script scrapes the text content from a website and saves it to a file.
"""
import os
import sys

# Add the project root to the Python path to allow for `src` imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# This will be replaced by the real tool in the agent environment
from src.tools_placeholder import view_text_website

def scrape_website_content(url: str, output_file: str):
    """
    Scrapes the text content of a website and saves it to a file.
    """
    print(f"Attempting to scrape content from {url}...")
    try:
        content = view_text_website(url)

        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully scraped content and saved to {output_file}")
        return True
    except Exception as e:
        print(f"Could not scrape website: {e}")
        print("Using the existing or placeholder brand_voice.txt file.")
        return False

if __name__ == "__main__":
    scrape_website_content("https://www.realmstoriches.xyz", "knowledge/brand_voice.txt")