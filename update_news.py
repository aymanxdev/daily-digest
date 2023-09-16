import os
import requests
from datetime import datetime

API_URL = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty"
NEWS_FILE_PATH = "daily_news.md"
README_PATH = "README.md"

# Fetch the IDs of the top stories
response = requests.get(API_URL)
top_stories = response.json()[:3]  # Fetch only top 3 stories

news_list = []

for story_id in top_stories:
    response = requests.get(ITEM_URL.format(story_id))
    item = response.json()
    news_list.append((item['title'], item['url']))

# Current date for the title
current_date = datetime.now().strftime('%Y-%m-%d')

# Determine if it's morning or afternoon/evening
current_hour = datetime.now().hour
if current_hour < 12:
    time_of_day = "Morning"
else:
    time_of_day = "Afternoon/Evening"

# Format data for Markdown
# formatted_data = "# Daily Dev News Summary\n\n"
formatted_data = f"## {time_of_day} Digest - {current_date}\n\n"
for title, url in news_list:
    formatted_data += f"- [{title}]({url})\n"

# Write to the news Markdown file
with open(NEWS_FILE_PATH, 'a') as f:  # Using 'a' to append the new digest to the existing content
    f.write(formatted_data)

# Update the main README to include a link to the news file
# You can remove this part if you don't want to update the main README every time.
with open(README_PATH, 'a') as readme:
    readme.write(f"\n[Click here for the {time_of_day} Digest - {current_date}](daily_news.md)")
