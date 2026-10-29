# Data Directory: `data/`

This directory manages test datasets, fixtures, and local SQLite database files, overseen by **TV2 (Data & Test Dataset)**.

---

## 1. Directory Structure & Git Tracking Policy

```text
data/
├── README.md               # This documentation file
├── samples/                # TRACKED in Git: Small, standardized benchmark fixtures
│   └── sample_small.json   # 2-warehouse, 3-order toy benchmark fixture
├── raw/                    # UNTRACKED in Git: Large synthetic generation or raw files
└── processed/              # UNTRACKED in Git: Pre-processed intermediate datasets
```

> **Security & Cleanliness Note:**  
> Large raw data files (`data/raw/*`), processed caches (`data/processed/*`), and active database files (`*.sqlite`, `*.db`) are strictly ignored in `.gitignore`.  
> Only verified sample fixtures inside `data/samples/` should be tracked in Git.

---

## 2. Sample Datasets Available

- `data/samples/sample_small.json`: Baseline toy benchmark matching the hand-calculated scenario in [docs/mathematical-model.md](../docs/mathematical-model.md).
