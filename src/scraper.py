"""
Scraping utilities for extracting football match results from Yallakora.com
for a given date.

IMPORTANT: Yallakora's HTML structure and class names can change over time.
If this scraper stops finding results, inspect the page in your browser's
DevTools and update SELECTORS below.

Always check a website's robots.txt and Terms of Service before scraping,
and add delays between requests if scraping multiple dates.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.yallakora.com"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}

# CSS selectors observed on Yallakora's match listing page.
# These may need updating if Yallakora changes its frontend.
SELECTORS = {
    "match_card": ("div", {"class": "item finish liItem"}),
    "channel": ("div", {"class": "channel icon-channel"}),
    "team_a": ("div", {"class": "teams teamA"}),
    "team_b": ("div", {"class": "teams teamB"}),
    "score": ("span", {"class": "score"}),
    "time": ("span", {"class": "time"}),
    "details_link": ("a", {"class": "button details"}),
}


def fetch_matches_page(date: str) -> BeautifulSoup:
    """
    Fetch the Yallakora matches page for a given date.

    Args:
        date (str): Date string in the form "MM/DD/YYYY", e.g. "11/23/2022".

    Returns:
        BeautifulSoup: Parsed HTML content.

    Raises:
        requests.HTTPError: If the request fails.
    """
    url = f"{BASE_URL}/matches?date={date}#day"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_matches(soup: BeautifulSoup) -> list:
    """
    Extract finished match details from a Yallakora matches page.

    Only matches with the "item finish liItem" card (i.e. completed matches
    with a final score) are extracted. Live or upcoming matches use a
    different card class and are not covered by this function.

    Args:
        soup (BeautifulSoup): Parsed HTML of a Yallakora matches page.

    Returns:
        list[dict]: One dict per match, with keys:
                     team_a, team_b, score, time, channel, link.
                     Fields that couldn't be found are set to None rather
                     than raising an error, so one malformed card doesn't
                     break the whole page.
    """
    tag, attrs = SELECTORS["match_card"]
    cards = soup.find_all(tag, attrs=attrs)

    matches = []
    for card in cards:
        match = {
            "team_a": None,
            "team_b": None,
            "score": None,
            "time": None,
            "channel": None,
            "link": None,
        }

        tag, attrs = SELECTORS["team_a"]
        team_a_el = card.find(tag, attrs=attrs)
        if team_a_el:
            match["team_a"] = team_a_el.get_text(strip=True)

        tag, attrs = SELECTORS["team_b"]
        team_b_el = card.find(tag, attrs=attrs)
        if team_b_el:
            match["team_b"] = team_b_el.get_text(strip=True)

        tag, attrs = SELECTORS["score"]
        score_els = card.find_all(tag, attrs=attrs)
        if len(score_els) >= 2:
            score_a = score_els[0].get_text(strip=True)
            score_b = score_els[1].get_text(strip=True)
            match["score"] = f"{score_a} - {score_b}"

        tag, attrs = SELECTORS["time"]
        time_el = card.find(tag, attrs=attrs)
        if time_el:
            match["time"] = time_el.get_text(strip=True)

        tag, attrs = SELECTORS["channel"]
        channel_el = card.find(tag, attrs=attrs)
        if channel_el:
            match["channel"] = channel_el.get_text(strip=True)

        tag, attrs = SELECTORS["details_link"]
        link_el = card.find(tag, attrs=attrs)
        if link_el and link_el.get("href"):
            match["link"] = BASE_URL + link_el["href"]

        matches.append(match)

    return matches


def scrape_matches_for_date(date: str) -> pd.DataFrame:
    """
    Fetch and parse all finished matches for a given date into a DataFrame.

    Args:
        date (str): Date string in the form "MM/DD/YYYY", e.g. "11/23/2022".

    Returns:
        pd.DataFrame: Columns: team_a, team_b, score, time, channel, link.
    """
    soup = fetch_matches_page(date)
    matches = parse_matches(soup)
    return pd.DataFrame(matches)
