import json
import csv
import os

# Input JSON file (latest file in data folder)
def get_latest_file():
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    files.sort(reverse=True)  # latest first
    return os.path.join("data", files[0])


def main():
    try:
        input_file = get_latest_file()
    except:
        print("No JSON file found in data folder")
        return

    print(f"Reading data from {input_file}...")

    # Load JSON data
    with open(input_file, "r") as f:
        data = json.load(f)

    cleaned_data = []
    seen_ids = set()  # for duplicate removal

    for story in data:

        # Skip duplicates
        if story["post_id"] in seen_ids:
            continue

        seen_ids.add(story["post_id"])

        # Handle missing values
        cleaned_story = {
            "post_id": story.get("post_id", ""),
            "title": story.get("title", "").strip(),
            "category": story.get("category", "unknown"),
            "score": story.get("score", 0),
            "num_comments": story.get("num_comments", 0),
            "author": story.get("author", "unknown"),
            "collected_at": story.get("collected_at", "")
        }

        # Skip empty titles (basic cleaning)
        if cleaned_story["title"] == "":
            continue

        cleaned_data.append(cleaned_story)

    # Output CSV file
    output_file = "data/cleaned_trends.csv"

    # Write CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cleaned_data[0].keys())
        writer.writeheader()
        writer.writerows(cleaned_data)

    print(f"\nCleaned {len(cleaned_data)} records.")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()