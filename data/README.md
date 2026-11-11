# Data Directory: `data/`

Curated datasets and future machine-readable schemas for LogiMind, overseen by
**TV2 (Data & Test Dataset)**. The authoritative field definitions are in
[`docs/data-dictionary.md`](../docs/data-dictionary.md); Policy A is described in
[`docs/mathematical-model.md`](../docs/mathematical-model.md).

## Directory structure

```text
data/
├── README.md
├── samples/                    # Tracked, curated fixtures
│   ├── benchmark_data.json     # Legacy prototype input (not Policy A)
│   └── sample_small.json       # Draft toy fixture (not yet Policy A)
└── schema/                     # Planned: machine-readable dataset schemas
```

`data/raw/` and `data/processed/` are local scratch areas and are ignored by Git
(see `.gitignore`). They may be created locally but are never committed.

## Fixtures

| File | Purpose | Contract status |
| :--- | :--- | :--- |
| [`samples/benchmark_data.json`](samples/benchmark_data.json) | Input for the standalone legacy prototype. Three warehouses, two orders, Euclidean distance costs, aggregate capacity. | **Legacy, not Policy A.** Documented in [Appendix A](../docs/data-dictionary.md#appendix-a-legacy-prototype-dataset-specification). |
| [`samples/sample_small.json`](samples/sample_small.json) | Early draft toy fixture from the repository scaffold. | **Draft, not yet Policy A.** It still contains split/unassigned penalty fields, `daily_capacity`, and `handling_cost_per_unit`; TV2 owns its replacement. |

Do not treat either fixture as the canonical Policy A benchmark contract. The
canonical Policy A schema, generator, validator, and edge-case fixtures are TV2
deliverables and are not present in this branch.

## Commands

Validate JSON syntax:

```bash
python -m json.tool data/samples/benchmark_data.json > /dev/null
python -m json.tool data/samples/sample_small.json > /dev/null
```

Run the legacy prototype against its fixture:

```bash
python scripts/validate_orders.py
```

## Tracking rules

- Commit only curated, reproducible fixtures under `data/samples/`.
- Put machine-readable schemas under `data/schema/`.
- Keep large/generated datasets in `data/raw/` or `data/processed/` locally.
- Never commit SQLite databases (`*.db`, `*.sqlite`, `*.sqlite3`), secrets, or
  extracted customer data.
- Record provenance (generator, seed, or source) in each fixture or in this
  README when adding a new dataset.
- Add edge cases deliberately; do not label a fixture feasible or infeasible
  without verification.
