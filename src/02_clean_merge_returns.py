"""
02_clean_merge_returns.py

Clean the MILA prices panel and compute log-returns.

Steps:
- Load data/processed/mila_prices.parquet
- Optionally drop days with excessive missing data
- Forward/backward fill within reasonable limits
- Compute log-returns
- Save to data/processed/mila_log_returns.parquet
"""

import pandas as pd

from utils import (
    ensure_directories,
    PROCESSED_DIR,
    compute_log_returns,
)


def clean_and_compute_returns(
    max_missing_ratio: float = 0.5
) -> None:
    """
    Clean the prices panel and compute log-returns.

    Parameters
    ----------
    max_missing_ratio : float
        Maximum allowed fraction of missing values per row.
        Rows with more missing values are dropped.
    """
    ensure_directories()
    prices_path = PROCESSED_DIR / "mila_prices.parquet"
    print(f"Loading prices from {prices_path} ...")
    prices = pd.read_parquet(prices_path)

    # Drop rows with too many NaNs
    frac_missing = prices.isna().mean(axis=1)
    keep_mask = frac_missing <= max_missing_ratio
    prices = prices.loc[keep_mask]

    # Fill internal gaps
    prices = prices.sort_index()
    prices = prices.ffill().bfill()

    # Compute log-returns
    log_ret = compute_log_returns(prices)

    out_path = PROCESSED_DIR / "mila_log_returns.parquet"
    log_ret.to_parquet(out_path)
    print(f"Saved MILA log-returns to {out_path}")
    print("Shape:", log_ret.shape)


if __name__ == "__main__":
    clean_and_compute_returns()
