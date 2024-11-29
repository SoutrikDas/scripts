import feedparser
import requests
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# List of RSS feeds to monitor
rss_feeds = [
    {"name": "Unchosen Champion",
        "url": "https://www.royalroad.com/fiction/syndication/62573"},
]

# Function to check if an entry is new
def is_new_entry(published_time):
    now = datetime.now(timezone.utc)
    time_difference = (now - published_time).total_seconds() / \
        60  # Difference in minutes
    return time_difference <= 5  # Consider new if published within the last 5 minutes


# Check each feed
for feed in rss_feeds:
    # Fetch RSS feed using requests
    response = requests.get(feed["url"])
    
    # Parse the feed content with feedparser
    feed_data = feedparser.parse(response.content)
    
    if feed_data.entries:
        latest_entry = feed_data.entries[0]
        published_str = latest_entry.get("published") or latest_entry.get("pubDate")
        print(f"published_str: {published_str}")
        
        if published_str:
            try:
                # Parse the published time and convert to UTC
                published_time = parsedate_to_datetime(published_str).astimezone(timezone.utc)
                
                # Check if the entry is new
                if is_new_entry(published_time):
                    # Send notification for a new entry
                    message = f"New Chapter in {feed['name']}"
                    print(f"message: {message}")

                    # Send the notification
                    requests.post(
                        "https://ntfy.sh/novelnotification",
                        data=message.encode("utf-8")
                    )
                    print(f"Notification sent: {message}")
                else:
                    print(f"No new entries in {feed['name']} within the last 5 minutes.")
            except Exception as e:
                print(f"Error parsing published time for {feed['name']}: {e}")
        else:
            print(f"No published date found in the latest entry for {feed['name']}.")
    else:
        print(f"No entries found in {feed['name']}.")
