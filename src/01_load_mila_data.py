"""
01_load_mila_data.py

Load MILA index data from Excel files downloaded from S&P Global and
build a single prices panel with aligned dates.

Output:
- data/processed/mila_prices.parquet
"""

from pathlib import Path

import pandas as pd

from utils import (
    ensure_directories,
    RAW_DIR,
    PROCESSED_DIR,
    INDEX_FILES,
    load_index_from_excel,
)


def build_mila_prices() -> None:
    ensure_directories()

    series_dict = {}

    for name, fname in INDEX_FILES.items():
        fpath = RAW_DIR / fname
        print(f"Loading {name} from {fpath} ...")
        s = load_index_from_excel(fpath)
        s.name = name
        series_dict[name] = s

    # Align on union of dates (outer join)
    df = pd.concat(series_dict.values(), axis=1, join="outer")
    df = df.sort_index()

    out_path = PROCESSED_DIR / "mila_prices.parquet"
    df.to_parquet(out_path)
    print(f"Saved MILA prices panel to {out_path}")
    print("Shape:", df.shape)


if __name__ == "__main__":
    build_mila_prices()
