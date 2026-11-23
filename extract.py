import time
import requests

API_KEY = "3YOUR_API_KEY_HERE"
URL = "https://api.rawg.io/api/games"

def extract_games(start_year=2010, end_year=2026):
    all_games = []  # Like std::vector in C++

    for year in range(start_year, end_year + 1):
        params = {
            "key": API_KEY,
            "dates": f"{year}-01-01,{year}-12-31",
            "ordering": "-added",
            "page_size": 40
        }

        response = requests.get(URL, params=params)

        if response.status_code == 200:
            games = response.json()["results"]
            all_games.extend(games)
            print(f"Year {year}: fetched {len(games)} games")
        else:
            print(f"Year {year}: failed (Status {response.status_code})")

        time.sleep(0.2)  # Short pause so we don't spam the API

    return all_games

# Only runs when you execute extract.py directly (like int main() in C++)
if __name__ == "__main__":
    raw_data = extract_games()
    print(f"\nTotal raw games extracted: {len(raw_data)}")