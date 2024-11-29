import feedparser
import requests

url = "https://www.royalroad.com/fiction/syndication/62573"

# Fetch RSS feed using requests
response = requests.get(url)

# Parse the feed content
feed = feedparser.parse(response.content)

