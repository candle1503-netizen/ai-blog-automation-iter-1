import os
import logging
import requests
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def fetch_article(url):
    """
    Fetch article content from URL.

    Args:
    - url (str): Article URL.

    Returns:
    - content (str): Article content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching article: {e}")
        return None

def summarize_article(text):
    """
    Summarize article text.

    Args:
    - text (str): Article text.

    Returns:
    - summary (str): Article summary.
    """
    # Implement article summarization logic here
    # For demonstration purposes, return a simple summary
    return text[:100] + "..."

def save_summaries(summaries):
    """
    Save article summaries to file.

    Args:
    - summaries (list): List of article summaries.
    """
    output_path = os.environ.get('OBSIDIAN_PATH', os.path.expanduser('~/Documents/Obsidian'))
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(os.path.join(output_path, "summaries.md"), "w") as f:
        for summary in summaries:
            f.write(f"### {summary['title']}\n")
            f.write(f"{summary['summary']}\n")
            f.write(f"[Read more]({summary['url']})\n\n")