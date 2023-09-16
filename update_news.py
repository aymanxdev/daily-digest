import os
import requests

API_URL = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty"
NEWS_FILE_PATH = "daily_news.md"
README_PATH = "README.md"

# Fetch the IDs of the top stories
response = requests.get(API_URL)
top_stories = response.json()[:5]

news_list = []

for story_id in top_stories:
    response = requests.get(ITEM_URL.format(story_id))
    item = response.json()
    news_list.append((item['title'], item['url']))

# Format data for Markdown
formatted_data = "# Daily Dev News Summary\n\n"
for title, url in news_list:
    formatted_data += f"- [{title}]({url})\n"

# Write to the news Markdown file
with open(NEWS_FILE_PATH, 'w') as f:
    f.write(formatted_data)

# Update the main README to include a link to the news file
with open(README_PATH, 'a') as readme:
    readme.write("\n[Click here for the latest daily dev news](daily_news.md)")
