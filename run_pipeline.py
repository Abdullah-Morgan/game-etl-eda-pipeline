from extract import extract_games
from transform_load import transform_and_load
from eda import run_eda

if __name__ == "__main__":
    print("--- STEP 1: EXTRACT ---")
    raw_games = extract_games(2010, 2026)

    print("\n--- STEP 2: TRANSFORM & LOAD ---")
    transform_and_load(raw_games)

    print("\n--- STEP 3: EDA ---")
    run_eda()