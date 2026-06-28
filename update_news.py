import requests
from datetime import datetime

API_URL = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty"
NEWS_FILE_PATH = "daily_news.md"


def fetch_top_stories(limit=3):
    """Return a list of (title, url) tuples for the current top HN stories."""
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    top_ids = response.json()[:limit]

    stories = []
    for story_id in top_ids:
        item = requests.get(ITEM_URL.format(story_id), timeout=30).json()
        # Some stories (e.g. "Ask HN") have no external URL; fall back to the
        # Hacker News discussion link so we never KeyError.
        url = item.get("url", f"https://news.ycombinator.com/item?id={story_id}")
        stories.append((item["title"], url))
    return stories


def format_digest(stories, now=None):
    """Render a list of (title, url) tuples as a dated Markdown digest block."""
    now = now or datetime.now()
    time_of_day = "Morning" if now.hour < 12 else "Afternoon/Evening"
    current_date = now.strftime("%d-%m-%Y")

    block = f"## {time_of_day} Digest - {current_date}\n\n"
    for title, url in stories:
        block += f"- [{title}]({url})\n"
    return block


def main():
    stories = fetch_top_stories()
    block = format_digest(stories)
    with open(NEWS_FILE_PATH, "a") as file:
        file.write(block)


if __name__ == "__main__":
    main()
