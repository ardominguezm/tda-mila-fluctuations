# Topological Data Analysis to Characterize Fluctuations in the Latin American Integrated Market (MILA)

This repository contains the full reproducible workflow for the study:

**Domínguez Monterroza, A., Mateos Caballero, A., Jiménez-Martín, A. (2023).** *Topological Data Analysis to Characterize Fluctuations in the Latin American Integrated Market.* In: Figueroa-García, J.C., Hernández, G., Villa Ramirez, J.L., Gaona García, E.E. (eds)  **Applied Computer Sciences in Engineering.** WEA 2023.  Communications in Computer and Information Science, vol **1928**, Springer, Cham. https://doi.org/10.1007/978-3-031-46739-4_18

---

## Funding

This work was supported by the Spanish Ministry of Science and Innovation projects
*PID2021-122209OB-C31* and *RED2022-134540-T*.

---

## Data Source

All market data used in this study were obtained from:

**S&P Dow Jones Indices (S&P Global)**  
https://www.spglobal.com/spdji/en/regional-exposure/americas/#overview

The indices included in the MILA region are:

- **S&P/BMV IPC – Mexico**  
- **S&P/BVL Select – Peru**  
- **S&P/CLX IPSA – Chile**  
- **S&P Colombia Select – Colombia**

Data were downloaded as historical price Excel files directly from S&P Global’s regional exposure portal.

---

## Overview

This repository provides a complete **Topological Data Analysis (TDA)** pipeline to study fluctuations and structural dynamics in the **Latin American Integrated Market (MILA)**.

The analysis includes:

- Construction of **log-return time series**  
- Sliding-window embedding of multivariate returns  
- Construction of **Vietoris–Rips filtrations**  
- Extraction of **persistent homology (H₀, H₁)**  
- Computation of **persistence landscapes** (L¹ and L² norms)  
- Visualization of topological descriptors across time  
- Reproduction of figures included in the Springer CCIS paper

The focus is on identifying **structural changes**, **co-movement patterns**, and **topology-driven indicators of market fluctuations**.

---

## Repository Structure

```
tda-mila-fluctuations/
│
├── data/
│   ├── raw/                # Raw Excel files downloaded from S&P Global
│   └── processed/          # Cleaned prices, log-returns, windows, persistence outputs
│
├── src/
│   ├── 01_load_mila_data.py
│   ├── 02_clean_merge_returns.py
│   ├── 03_sliding_windows.py
│   ├── 04_compute_persistence.py
│   ├── 05_persistence_landscapes.py
│   ├── 06_generate_figures.py
│   └── utils.py
│
├── notebooks/
│   └── TDA_MILA.ipynb      # Minimal and reproducible TDA workflow
│
├── results/
│   └── figures/            # Figures generated for the article
│
├── CITATION.cff
└── README.md
```

---

## Requirements

The following Python packages are required:

- numpy  
- pandas  
- matplotlib  
- scikit-learn  
- ripser  
- persim  
- gudhi (optional alternative backend)  
- tqdm  

A reproducible environment file (`environment.yml`) is included.

---

## Reproducibility

To reproduce the full analysis:

```bash
conda env create -f environment.yml
conda activate tda-mila
python src/01_load_mila_data.py
python src/02_clean_merge_returns.py
python src/03_sliding_windows.py
python src/04_compute_persistence.py
python src/05_persistence_landscapes.py
python src/06_generate_figures.py
```

---

##  License

MIT License.

---

If you use this repository, please cite the original Springer publication.
