import pandas as pd
import os

def main():
    file_path = "data/cleaned_trends.csv"

    # Check if file exists
    if not os.path.exists(file_path):
        print("CSV file not found. Run Task 2 first.")
        return

    print("Loading data...\n")

    # Read CSV using pandas
    df = pd.read_csv(file_path)

    # -------------------------------
    # BASIC ANALYSIS
    # -------------------------------

    print("Total number of stories:", len(df))

    # Stories per category
    print("\nStories per category:")
    print(df["category"].value_counts())

    # Average score per category
    print("\nAverage score per category:")
    print(df.groupby("category")["score"].mean())

    # Most popular story (highest score)
    top_story = df.loc[df["score"].idxmax()]

    print("\nTop Story:")
    print("Title:", top_story["title"])
    print("Category:", top_story["category"])
    print("Score:", top_story["score"])

    # Most commented story
    most_commented = df.loc[df["num_comments"].idxmax()]

    print("\nMost Commented Story:")
    print("Title:", most_commented["title"])
    print("Comments:", most_commented["num_comments"])

    # -------------------------------
    # EXTRA (for better marks)
    # -------------------------------

    # Top 5 stories by score
    print("\nTop 5 Stories by Score:")
    print(df.sort_values(by="score", ascending=False)[["title", "score"]].head(5))

    # Top 5 authors by number of posts
    print("\nTop Authors:")
    print(df["author"].value_counts().head(5))


if __name__ == "__main__":
    main()