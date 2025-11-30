"""
05_persistence_landscapes.py

Compute persistence landscapes and their norms (L1 and L2) for each window.

Uses:
- H1 diagrams saved in results/persistence/H1_window_<k>.npy
- Metadata in data/processed/mila_windows_metadata.parquet

Outputs:
- results/landscapes/mila_landscape_norms.parquet
"""

from pathlib import Path

import numpy as np
import pandas as pd
from persim import PersistenceLandscape

from utils import (
    ensure_directories,
    PROCESSED_DIR,
    PERSISTENCE_DIR,
    LANDSCAPES_DIR,
)


def compute_landscape_norms() -> None:
    ensure_directories()

    meta_path = PROCESSED_DIR / "mila_windows_metadata.parquet"
    print(f"Loading window metadata from {meta_path} ...")
    meta = pd.read_parquet(meta_path)

    records = []

    for _, row in meta.iterrows():
        idx = int(row["window_index"])
        start_date = row["start_date"]
        end_date = row["end_date"]

        dgm_path = PERSISTENCE_DIR / f"H1_window_{idx}.npy"
        if not dgm_path.exists():
            print(f"Warning: diagram not found for window {idx}, skipping.")
            continue

        H1 = np.load(dgm_path)

        if H1.shape[0] == 0:
            L1_norm = 0.0
            L2_norm = 0.0
        else:
            # Build a persistence landscape from the H1 diagram
            pl = PersistenceLandscape(dgms=[H1])
            # L1 and L2 norms of the landscape
            L1_norm = pl.p_norm(p=1)
            L2_norm = pl.p_norm(p=2)

        records.append(
            {
                "window_index": idx,
                "start_date": start_date,
                "end_date": end_date,
                "L1_norm": float(L1_norm),
                "L2_norm": float(L2_norm),
            }
        )

    norms_df = pd.DataFrame(records).sort_values("window_index")
    out_path = LANDSCAPES_DIR / "mila_landscape_norms.parquet"
    norms_df.to_parquet(out_path)
    print(f"Saved landscape norms to {out_path}")
    print("Shape:", norms_df.shape)


if __name__ == "__main__":
    compute_landscape_norms()
