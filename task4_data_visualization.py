import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    file_path = "data/cleaned_trends.csv"

    # Check if file exists
    if not os.path.exists(file_path):
        print("CSV file not found. Run Task 2 first.")
        return

    print("Loading data...")

    df = pd.read_csv(file_path)

    # Create output folder for graphs
    if not os.path.exists("data/plots"):
        os.makedirs("data/plots")

    # -------------------------------
    # 1. Stories per Category (Bar Chart)
    # -------------------------------
    category_counts = df["category"].value_counts()

    plt.figure()
    category_counts.plot(kind="bar")
    plt.title("Number of Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.xticks(rotation=45)

    plt.savefig("data/plots/category_distribution.png")
    plt.close()

    # -------------------------------
    # 2. Average Score per Category
    # -------------------------------
    avg_scores = df.groupby("category")["score"].mean()

    plt.figure()
    avg_scores.plot(kind="bar")
    plt.title("Average Score per Category")
    plt.xlabel("Category")
    plt.ylabel("Average Score")
    plt.xticks(rotation=45)

    plt.savefig("data/plots/avg_score.png")
    plt.close()

    # -------------------------------
    # 3. Top 10 Stories by Score
    # -------------------------------
    top_stories = df.sort_values(by="score", ascending=False).head(10)

    plt.figure()
    plt.barh(top_stories["title"], top_stories["score"])
    plt.title("Top 10 Stories by Score")
    plt.xlabel("Score")
    plt.ylabel("Title")

    plt.savefig("data/plots/top_stories.png")
    plt.close()

    print("\nGraphs saved in data/plots/ folder")


if __name__ == "__main__":
    main()