# Yallakora Matches Scraper ⚽

A web scraping project that extracts football match results — teams, final score, kickoff time, TV broadcasting channel, and match details link — from [Yallakora.com](https://www.yallakora.com) for any given date.

## ⚠️ A Note on Selector Stability

Website structures can change over time. If this scraper returns zero results, the class names in `src/scraper.py` may no longer match the live site.

**If that happens:**
1. Open the [matches page](https://www.yallakora.com/matches) for a date you know has finished matches.
2. Right-click a finished match card → "Inspect" (DevTools).
3. Confirm the current class names (e.g. `item finish liItem`, `teams teamA`, `score`).
4. Update the `SELECTORS` dictionary at the top of `src/scraper.py`.

The parsing logic itself was tested against mock HTML built from real scraped output (matching the site's structure at the time this project was created) and works correctly as long as the selectors match the live site.

## 📌 Project Overview

- Prompt for a date (`MM/DD/YYYY`) and fetch that day's matches page
- Extract only **finished** matches: both team names, final score, kickoff time, TV channel, and a link to match details
- Clean the scraped data (drop failed parses, remove duplicates)
- Split the combined score (e.g. "3 - 0") into separate numeric columns for easier analysis
- Export to CSV (UTF-8 with BOM, so Arabic team names display correctly in Excel)

## 🗂️ Project Structure

```
yallakora-matches-scraper/
├── data/                       # Scraped CSV output goes here (gitignored)
├── notebooks/
│   └── yallakora_matches_scraper.ipynb   # Full walkthrough notebook
├── src/
│   ├── scraper.py              # Fetching & parsing match data
│   └── cleaning.py             # Deduplication & score splitting
├── main.py                     # Runs the full scrape end-to-end (prompts for a date)
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/yallakora-matches-scraper.git
cd yallakora-matches-scraper
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the scraper
```bash
python main.py
```
You'll be prompted to enter a date (e.g. `11/23/2022`). Results are saved to `data/yallakora_matches_<date>.csv`.

Or explore step-by-step in the notebook:
```bash
jupyter notebook notebooks/yallakora_matches_scraper.ipynb
```

## ⚖️ Responsible Scraping

- Check [yallakora.com/robots.txt](https://www.yallakora.com/robots.txt) and Yallakora's Terms of Service before scraping at scale.
- Avoid sending rapid, repeated requests — space out calls if scraping multiple dates in a loop.
- This project is for educational/personal data analysis purposes.

## 🛠️ Tech Stack

- Python
- Requests (HTTP requests)
- BeautifulSoup4 (HTML parsing)
- Pandas (data handling)

## 📄 License

This project is open source and available under the [MIT License](LICENSE). Scraped data belongs to its original source (Yallakora) — respect the site's terms of use.
