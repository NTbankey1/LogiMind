# Automation Scripts Directory: `scripts/`

This directory stores developer utility scripts, dataset generators, and verification helpers.

---

## 1. Planned Scripts

| Script Name | Owner | Purpose |
| :--- | :--- | :--- |
| `generate_synthetic_orders.py` | TV2 | Generates randomized realistic order volumes, SKU distributions, and distance matrices. |
| `validate_datasets.py` | TV2 & TV6 | Validates JSON/CSV datasets against schema definitions in `docs/data-dictionary.md`. |
| `seed_database.py` | TV5 | Loads sample datasets into the local SQLite database. |
| `run_benchmarks.py` | TV3 & TV6 | Runs automated comparative runs between Baseline and MILP and outputs markdown tables. |
