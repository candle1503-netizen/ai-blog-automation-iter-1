# Assuming the fetcher, summarizer, and writer modules are implemented correctly
from fetcher import fetch_hn_top, fetch_github_trending, save_articles
from summarizer import fetch_article, summarize_article, save_summaries
from writer import fetch_articles, generate_post, save_post
import os
import logging
import requests
import time
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def extract_text_from_html(html):
    """
    Extract text from HTML content.

    Args:
    - html (str): HTML content.

    Returns:
    - text (str): Extracted text.
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def run_automation(max_retries=3, retry_delay=60):
    """
    Run the automation process with retry mechanism.

    Args:
    - max_retries (int): Maximum number of retries.
    - retry_delay (int): Delay between retries in seconds.
    """
    retries = 0
    while retries <= max_retries:
        try:
            # Fetch articles from Hacker News and GitHub trending
            hn_articles = fetch_hn_top()
            github_articles = fetch_github_trending()
            
            # Save articles to file
            save_articles(hn_articles + github_articles)
            
            # Fetch articles from file
            articles = fetch_articles()
            
            # Summarize articles
            summaries = []
            for article in articles:
                try:
                    # Fetch article content
                    article_content = fetch_article(article['url'])
                    # Extract text from HTML
                    text = extract_text_from_html(article_content)
                    # Summarize article
                    summary = summarize_article(text)
                    summaries.append({'title': article['title'], 'summary': summary, 'url': article['url']})
                except Exception as e:
                    logging.error(f"Error summarizing article: {e}")
            
            # Save summaries to file
            save_summaries(summaries)
            
            # Generate blog post
            post = generate_post(summaries)
            
            # Save post to file
            output_path = os.environ.get('OBSIDIAN_PATH', os.path.expanduser('~/Documents/Obsidian'))
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            save_post(post, output_path)
            
            # If successful, break the loop
            break
        
        except Exception as e:
            logging.error(f"Error running automation: {e}")
            retries += 1
            if retries <= max_retries:
                logging.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error(f"Maximum retries exceeded. Automation failed.")

if __name__ == "__main__":
    run_automation()