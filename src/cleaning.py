"""
Cleaning utilities for the scraped Yallakora match data.
"""

import pandas as pd


def clean_matches(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw scraped matches dataframe:
    - Drop rows missing both team names (failed parses)
    - Drop exact duplicate rows
    - Reset the index

    Args:
        df (pd.DataFrame): Raw scraped matches dataframe.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    df = df.dropna(subset=["team_a", "team_b"], how="all").copy()
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df


def split_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split the combined 'score' column (e.g. "3 - 0") into two numeric
    columns: 'score_a' and 'score_b'.

    Args:
        df (pd.DataFrame): Dataframe with a 'score' column formatted as
                            "X - Y".

    Returns:
        pd.DataFrame: Dataframe with added 'score_a' and 'score_b' integer
                      columns (NaN where the score couldn't be parsed).
    """
    df = df.copy()
    split_scores = df["score"].str.split(" - ", expand=True)
    df["score_a"] = pd.to_numeric(split_scores[0], errors="coerce")
    df["score_b"] = pd.to_numeric(split_scores[1], errors="coerce")
    return df
