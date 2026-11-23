# Video Game Quality Trends (2010–2026) — ETL + EDA Pipeline

An end-to-end Python ETL (Extract, Transform, Load) and Exploratory Data Analysis (EDA) pipeline that analyzes the top 5 highest user-rated video games per year from 2010 to 2026 using the RAWG Video Games Database API, paired with an interactive web dashboard.

## Pipeline Architecture
1. **Extract (`extract.py`):** Queries the RAWG API for the top 40 most popular releases per year (2010–2026).
2. **Transform & Load (`transform_load.py`):** Validates raw JSON records with **Pydantic** (`GameModel`), cleans and parses release dates with **Pandas**, filters to the top 5 user-rated games per year (85 games total), and saves the result to `top_games_2010_2026.csv`.
3. **EDA (`eda.py`):** Computes yearly average user ratings, total player engagement (`ratings_count`), identifies the #1 game per year, generates `eda_charts.png` with **Matplotlib**, and exports `data.json` for the web dashboard.
4. **Dashboard (`index.html`):** Interactive static web app displaying KPI cards, Chart.js visualizations, year-by-year tabs, and a full search/sort table.

## How to Run Locally
```bash
pip install requests pydantic pandas matplotlib

```

Add your RAWG API key in `extract.py`, then run:
```bash
python run_pipeline.py
```