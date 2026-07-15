"""
End-to-end scraping pipeline for Yallakora match results on a given date.

Run with:
    python main.py
And enter a date when prompted, in the form MM/DD/YYYY.

Output is saved to data/yallakora_matches_<date>.csv
"""

import os

from src.cleaning import clean_matches, split_score
from src.scraper import scrape_matches_for_date


def main():
    date = input("Enter the date as MM/DD/YYYY: ").strip()

    print(f"Scraping Yallakora matches for {date}...")
    df = scrape_matches_for_date(date)
    print(f"Raw scraped rows: {len(df)}")

    df = clean_matches(df)
    df = split_score(df)
    print(f"Cleaned rows: {len(df)}")
    print(df)

    os.makedirs("data", exist_ok=True)
    safe_date = date.replace("/", "-")
    output_path = f"data/yallakora_matches_{safe_date}.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\nSaved results to {output_path}")


if __name__ == "__main__":
    main()
