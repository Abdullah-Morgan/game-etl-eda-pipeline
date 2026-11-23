import json
import pandas as pd
import matplotlib.pyplot as plt

def run_eda(csv_path="top_games_2010_2026.csv"):
    df = pd.read_csv(csv_path)

    # 1. Yearly average user rating & total ratings count
    yearly = df.groupby("release_year").agg(
        avg_rating=("rating", "mean"),
        total_ratings_count=("ratings_count", "sum"),
        game_count=("name", "count")
    ).reset_index()
    yearly["avg_rating"] = yearly["avg_rating"].round(2)

    # 2. Top #1 game of each year
    top_per_year = df.sort_values(
        by=["release_year", "rating", "ratings_count"],
        ascending=[True, False, False]
    ).groupby("release_year").first().reset_index()

    yearly = yearly.merge(
        top_per_year[["release_year", "name", "rating"]].rename(
            columns={"name": "top_game_name", "rating": "top_game_rating"}
        ),
        on="release_year"
    )

    # Print EDA summary to terminal
    best_year_row = yearly.sort_values(by="avg_rating", ascending=False).iloc[0]
    best_game_row = df.sort_values(by=["rating", "ratings_count"], ascending=[False, False]).iloc[0]

    print("\n=== EDA SUMMARY ===")
    print(f"Best Year in Gaming: {int(best_year_row['release_year'])} (Avg Rating: {best_year_row['avg_rating']}/5)")
    print(f"Highest Rated Game Overall: {best_game_row['name']} ({best_game_row['rating']}/5 in {int(best_game_row['release_year'])})")
    print("\nTop 5 Years by Average Rating:")
    print(yearly.sort_values(by="avg_rating", ascending=False)[["release_year", "avg_rating", "total_ratings_count", "top_game_name"]].head(5).to_string(index=False))

    # 3. Save Matplotlib chart for repo/report
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    ax1.plot(yearly["release_year"], yearly["avg_rating"], marker="o", color="#6366f1", linewidth=2)
    ax1.set_title("Average User Rating of Top 5 Games per Year (2010–2026)")
    ax1.set_ylabel("Avg User Rating (0–5)")
    ax1.grid(True, alpha=0.3)

    ax2.bar(yearly["release_year"], yearly["total_ratings_count"], color="#10b981")
    ax2.set_title("Total Player Engagement (Ratings Count per Year)")
    ax2.set_xlabel("Release Year")
    ax2.set_ylabel("Total Ratings Count")
    ax2.grid(True, axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("eda_charts.png", dpi=150)
    print("\nSaved chart to eda_charts.png")

    # 4. Export data.json for the Vercel web app
    web_data = {
        "summary": {
            "best_year": int(best_year_row["release_year"]),
            "best_year_avg": float(best_year_row["avg_rating"]),
            "top_game_name": str(best_game_row["name"]),
            "top_game_rating": float(best_game_row["rating"]),
            "top_game_year": int(best_game_row["release_year"]),
            "total_games": int(len(df)),
            "overall_avg_rating": round(float(df["rating"].mean()), 2)
        },
        "yearly": yearly.to_dict(orient="records"),
        "games": df.to_dict(orient="records")
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(web_data, f, indent=2)
    print("Exported data.json for web dashboard!")

if __name__ == "__main__":
    run_eda()