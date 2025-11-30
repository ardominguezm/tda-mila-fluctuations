"""
03_sliding_windows.py

Create sliding windows from the MILA log-returns.

Each window is a T x d matrix (T = window_size, d = number of indices).

Outputs:
- data/processed/mila_windows_metadata.parquet (window_index, start_date, end_date)
(For TDA we will recompute windows on the fly using utils.sliding_windows, so
this script mainly provides metadata and a sanity check.)
"""

import pandas as pd

from utils import (
    ensure_directories,
    PROCESSED_DIR,
    sliding_windows,
)


def build_windows_metadata(window_size: int = 50, step: int = 1) -> None:
    ensure_directories()
    logret_path = PROCESSED_DIR / "mila_log_returns.parquet"
    print(f"Loading log-returns from {logret_path} ...")
    log_ret = pd.read_parquet(logret_path)

    windows = sliding_windows(log_ret, window_size=window_size, step=step)
    records = []
    for idx, (dates, _) in enumerate(windows):
        records.append(
            {
                "window_index": idx,
                "start_date": dates[0],
                "end_date": dates[-1],
            }
        )

    meta_df = pd.DataFrame(records)
    out_path = PROCESSED_DIR / "mila_windows_metadata.parquet"
    meta_df.to_parquet(out_path)
    print(f"Saved window metadata to {out_path}")
    print("Number of windows:", len(meta_df))


if __name__ == "__main__":
    build_windows_metadata(window_size=50, step=1)
