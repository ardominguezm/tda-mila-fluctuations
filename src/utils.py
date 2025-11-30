"""
utils.py

Utility functions and global configuration for the TDA analysis of the
Latin American Integrated Market (MILA).
"""

from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd


# -------------------------------------------------------------------
# Paths & directories
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
PERSISTENCE_DIR = RESULTS_DIR / "persistence"
LANDSCAPES_DIR = RESULTS_DIR / "landscapes"

# Excel file names for the four MILA indices (adjust if needed)
INDEX_FILES: Dict[str, str] = {
    "MEXICO": "sp-bvm-mexico.xlsx",
    "PERU": "sp-bvl_select-peru.xlsx",
    "CHILE": "sp-ipsa-chile.xlsx",
    "COLOMBIA": "sp-select-colombia.xlsx",
}


def ensure_directories() -> None:
    """Create all required directories if they do not exist."""
    for d in [
        DATA_DIR, RAW_DIR, PROCESSED_DIR,
        RESULTS_DIR, FIGURES_DIR, PERSISTENCE_DIR, LANDSCAPES_DIR
    ]:
        d.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------------------
# Data helpers
# -------------------------------------------------------------------

def load_index_from_excel(path: Path) -> pd.Series:
    """
    Load a single index level time series from an Excel file.

    The function tries several common column name patterns for date and index level.

    Parameters
    ----------
    path : Path
        Path to the Excel file.

    Returns
    -------
    series : pd.Series
        Time series with DatetimeIndex and float values.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    df = pd.read_excel(path)

    # Try to guess date column
    possible_date_cols = ["Date", "DATE", "date", "Trading Day", "Cal. Date"]
    date_col = None
    for c in df.columns:
        if c in possible_date_cols:
            date_col = c
            break
    if date_col is None:
        # Fallback: assume first column is date-like
        date_col = df.columns[0]

    # Try to guess level/price column (last non-date column)
    non_date_cols = [c for c in df.columns if c != date_col]
    if not non_date_cols:
        raise ValueError(f"No numeric column found in {path}")
    level_col = non_date_cols[-1]

    series = df[[date_col, level_col]].copy()
    series[date_col] = pd.to_datetime(series[date_col])
    series = series.set_index(date_col).sort_index()
    series = series[level_col].astype(float)

    # Drop obvious missing rows
    series = series.dropna()
    return series


def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Compute log returns from a prices DataFrame.

    Parameters
    ----------
    prices : pd.DataFrame
        Wide DataFrame with index=dates and columns=indices.

    Returns
    -------
    log_returns : pd.DataFrame
        One-step log returns.
    """
    return np.log(prices / prices.shift(1)).dropna(how="all")


def sliding_windows(
    df: pd.DataFrame,
    window_size: int,
    step: int = 1
) -> List[Tuple[pd.DatetimeIndex, pd.DataFrame]]:
    """
    Generate sliding windows over the rows of a time-indexed DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Time-indexed DataFrame (T x d).
    window_size : int
        Number of rows per window.
    step : int
        Step between windows (in rows).

    Returns
    -------
    windows : list of (index, df_window)
        Each element is a pair (DatetimeIndex, DataFrame window).
    """
    idx = df.index
    windows = []
    for start in range(0, len(df) - window_size + 1, step):
        end = start + window_size
        wdf = df.iloc[start:end]
        windows.append((wdf.index, wdf))
    return windows
