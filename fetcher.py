import os
import logging
import requests

# Set up logging
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def fetch_hn_top():
    """
    Fetch top articles from Hacker News.

    Returns:
    - articles (list): List of top articles.
    """
    try:
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json")
        response.raise_for_status()
        top_stories = response.json()
        articles = []
        for story_id in top_stories[:10]:
            response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
            response.raise_for_status()
            story = response.json()
            articles.append({"title": story["title"], "url": story["url"]})
        return articles
    except requests.RequestException as e:
        logging.error(f"Error fetching top articles: {e}")
        return []

def fetch_github_trending():
    """
    Fetch trending repositories from GitHub.

    Returns:
    - repositories (list): List of trending repositories.
    """
    try:
        response = requests.get("https://github.com/trending")
        response.raise_for_status()
        return []
    except requests.RequestException as e:
        logging.error(f"Error fetching trending repositories: {e}")
        return []

def save_articles(articles):
    """
    Save articles to file.

    Args:
    - articles (list): List of articles.
    """
    output_path = os.environ.get('OBSIDIAN_PATH', os.path.expanduser('~/Documents/Obsidian'))
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(os.path.join(output_path, "articles.md"), "w") as f:
        for article in articles:
            f.write(f"### {article['title']}\n")
            f.write(f"[Read more]({article['url']})\n\n")