import pandas as pd
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

# Pydantic schema to enforce strict types (like a C++ struct)
class GameModel(BaseModel):
    name: str = Field(min_length=1)
    released: Optional[str] = None
    rating: float = Field(ge=0.0, le=5.0)
    ratings_count: int = Field(ge=0)

def transform_and_load(raw_games, output_csv="top_games_2010_2026.csv"):
    valid_games = []

    # 1. Validate with Pydantic
    for item in raw_games:
        try:
            game = GameModel(**item)
            if game.released and game.rating > 0:
                valid_games.append(game.model_dump())
        except ValidationError:
            continue

    # 2. Transform with Pandas
    df = pd.DataFrame(valid_games)
    df["released"] = pd.to_datetime(df["released"], errors="coerce")
    df = df.dropna(subset=["released"])
    df["release_year"] = df["released"].dt.year.astype(int)
    df["released"] = df["released"].dt.strftime("%Y-%m-%d")

    # Keep only 2010-2026 and remove duplicate game titles
    df = df[(df["release_year"] >= 2010) & (df["release_year"] <= 2026)]
    df = df.drop_duplicates(subset=["name"])

    # Sort by highest user rating (tie-breaker: ratings_count) and keep Top 5 per year
    df = df.sort_values(
        by=["release_year", "rating", "ratings_count"],
        ascending=[True, False, False]
    )
    top5_df = df.groupby("release_year", as_index=False).head(5)

    # Reorder columns cleanly
    top5_df = top5_df[["release_year", "name", "released", "rating", "ratings_count"]]

    # 3. Load to CSV
    top5_df.to_csv(output_csv, index=False)
    print(f"Saved {len(top5_df)} cleaned games to {output_csv}")
    return top5_df