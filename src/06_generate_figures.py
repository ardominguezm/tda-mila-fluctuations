"""
06_generate_figures.py

Generate figures for the MILA TDA analysis:

- Time series of L1 and L2 norms of persistence landscapes across windows.
- (Optionally) example landscape for a selected window.

Figures are saved to results/figures/.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from persim import PersistenceLandscape

from utils import (
    ensure_directories,
    FIGURES_DIR,
    LANDSCAPES_DIR,
    PERSISTENCE_DIR,
)


def figure_landscape_norms() -> None:
    ensure_directories()
    norms_path = LANDSCAPES_DIR / "mila_landscape_norms.parquet"
    print(f"Loading landscape norms from {norms_path} ...")
    norms = pd.read_parquet(norms_path)

    # Use end_date as time coordinate
    t = pd.to_datetime(norms["end_date"])
    L1 = norms["L1_norm"].values
    L2 = norms["L2_norm"].values

    plt.figure(figsize=(10, 4))
    plt.plot(t, L1, label="L1 norm")
    plt.plot(t, L2, label="L2 norm")
    plt.xlabel("Time")
    plt.ylabel("Landscape norm")
    plt.title("Persistence Landscape Norms (H1) over time")
    plt.legend()
    plt.tight_layout()
    out_path = FIGURES_DIR / "mila_landscape_norms_time_series.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved figure to {out_path}")


def figure_example_landscape(window_index: int = 0) -> None:
    ensure_directories()

    dgm_path = PERSISTENCE_DIR / f"H1_window_{window_index}.npy"
    if not dgm_path.exists():
        print(f"Diagram for window {window_index} not found.")
        return

    H1 = np.load(dgm_path)
    if H1.shape[0] == 0:
        print(f"No H1 features for window {window_index}.")
        return

    pl = PersistenceLandscape(dgms=[H1])
    xs = np.linspace(H1[:, 0].min(), H1[:, 1].max(), 500)
    ys = pl(xs)

    plt.figure(figsize=(8, 4))
    for k in range(ys.shape[0]):
        plt.plot(xs, ys[k, :])
    plt.xlabel("Filtration value")
    plt.ylabel("Landscape value")
    plt.title(f"Persistence Landscape (H1) – Window {window_index}")
    plt.tight_layout()
    out_path = FIGURES_DIR / f"mila_landscape_example_win{window_index}.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved example landscape figure to {out_path}")


def generate_all_figures() -> None:
    figure_landscape_norms()
    # You can pick representative windows to visualize:
    figure_example_landscape(window_index=0)


if __name__ == "__main__":
    generate_all_figures()
