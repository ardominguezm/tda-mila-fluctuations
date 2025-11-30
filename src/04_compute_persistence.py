"""
04_compute_persistence.py

Compute persistent homology for each sliding window of MILA log-returns.

For each window:
- Build a point cloud (T x d) from the multivariate log-returns
- Use ripser to compute persistence diagrams
- Save H1 diagrams for later use in persistence landscapes

Outputs:
- results/persistence/H1_window_<k>.npy  (array of birth-death pairs for H1)
"""

import numpy as np
import pandas as pd
from ripser import ripser

from utils import (
    ensure_directories,
    PROCESSED_DIR,
    PERSISTENCE_DIR,
    sliding_windows,
)


def compute_persistence_for_windows(
    window_size: int = 50,
    step: int = 1,
    maxdim: int = 1
) -> None:
    ensure_directories()
    logret_path = PROCESSED_DIR / "mila_log_returns.parquet"
    print(f"Loading log-returns from {logret_path} ...")
    log_ret = pd.read_parquet(logret_path)

    windows = sliding_windows(log_ret, window_size=window_size, step=step)

    for idx, (dates, wdf) in enumerate(windows):
        X = wdf.values  # shape (T, d)

        # Compute persistent homology with ripser
        print(f"Computing persistence for window {idx} ({dates[0].date()} – {dates[-1].date()}) ...")
        out = ripser(X, maxdim=maxdim)
        dgms = out["dgms"]  # list of diagrams, dgms[0]=H0, dgms[1]=H1, ...

        # Save H1 diagram (if exists)
        if len(dgms) > 1 and dgms[1].size > 0:
            H1 = dgms[1]
        else:
            H1 = np.empty((0, 2))

        fpath = PERSISTENCE_DIR / f"H1_window_{idx}.npy"
        np.save(fpath, H1)

    print("Done computing persistence diagrams.")


if __name__ == "__main__":
    compute_persistence_for_windows(window_size=50, step=1, maxdim=1)
