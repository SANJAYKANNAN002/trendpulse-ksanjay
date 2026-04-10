import requests
import time
import json
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (as required)
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category based on title keywords
def get_category(title):
    title = title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title:
                return category
    return None  # no match


def main():
    print("Fetching top stories...")

    try:
        # Added timeout to prevent hanging
        response = requests.get(TOP_STORIES_URL, headers=headers, timeout=5)

        if response.status_code != 200:
            print("Failed to fetch top stories (bad status code)")
            return

        story_ids = response.json()[:500]

    except requests.exceptions.RequestException:
        print("Failed to fetch top stories (request error)")
        return

    collected_data = []

    # Track how many per category
    category_count = {cat: 0 for cat in categories}

    # Loop category-wise (important for assignment requirement)
    for cat in categories:
        print(f"\nCollecting {cat} stories...")

        for story_id in story_ids:

            # Stop when 25 stories collected for this category
            if category_count[cat] >= 25:
                break

            try:
                # Added timeout here too
                story_response = requests.get(
                    ITEM_URL.format(story_id),
                    headers=headers,
                    timeout=5
                )

                # Skip bad responses
                if story_response.status_code != 200:
                    continue

                story = story_response.json()

            except requests.exceptions.RequestException:
                print(f"Skipped story {story_id} due to request error")
                continue

            # Skip invalid or missing title
            if not story or "title" not in story:
                continue

            assigned_category = get_category(story["title"])

            # Only include if it matches current category
            if assigned_category != cat:
                continue

            # Extract required fields
            story_data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": assigned_category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected_data.append(story_data)
            category_count[cat] += 1

        # Sleep AFTER finishing one category (as required)
        time.sleep(2)

    # Create data folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Generate filename with current date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save data to JSON file
    with open(filename, "w") as f:
        json.dump(collected_data, f, indent=4)

    print(f"\nCollected {len(collected_data)} stories.")
    print(f"Saved to {filename}")


if __name__ == "__main__":
    main()