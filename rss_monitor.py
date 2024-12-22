import feedparser
import requests
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# List of RSS feeds to monitor
rss_feeds = [
    {
        "name": "Unchosen Champion",
        "url": "https://www.royalroad.com/fiction/syndication/62573",
    },
    {
        "name": "Super Supportive",
        "url": "https://www.royalroad.com/fiction/syndication/63759",
    },
    {
        "name": "Zenith of Sorcery",
        "url": "https://www.royalroad.com/fiction/syndication/71045",
    },
]


# Function to get the formatted time difference
def format_time_difference(time_difference):
    # Convert time difference to seconds
    total_seconds = time_difference.total_seconds()

    if total_seconds < 60:
        # If less than a minute, display seconds
        return f"{int(total_seconds)} seconds ago"
    elif total_seconds < 3600:
        # If less than an hour, display minutes
        minutes = total_seconds // 60
        return f"{int(minutes)} minutes ago"
    elif total_seconds < 172800:
        # If less than two days, display hours
        hours = total_seconds // 3600
        return f"{int(hours)} hours ago"
    else:
        # If more than two days, display days
        days = total_seconds // 86400
        return f"{int(days)} days ago"


# Check each feed
for feed in rss_feeds:
    # Fetch the RSS feed using requests
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
                published_time = parsedate_to_datetime(published_str).astimezone(
                    timezone.utc
                )
                time_difference = datetime.now(timezone.utc) - published_time

                # Get formatted time difference
                formatted_time = format_time_difference(time_difference)

                # Check if the time difference is within the last 20 minutes
                if time_difference.total_seconds() <= 20 * 60:
                    # Send notification for a new entry
                    message = f"New Chapter in {feed['name']}"
                    print(f"message: {message}")
                    requests.post(
                        "https://ntfy.sh/novelnotification",
                        data=message.encode("utf-8"),
                    )
                    print(f"Notification sent: {message}")
                else:
                    print(
                        f"No new entries in {feed['name']} within the last 20 minutes. Last entry was {formatted_time}."
                    )
            except Exception as e:
                print(f"Error parsing published time for {feed['name']}: {e}")
        else:
            print(f"No published date found in the latest entry for {feed['name']}.")
    else:
        print(f"No entries found in {feed['name']}.")
