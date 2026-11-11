# Data Directory: `data/`

Curated datasets, canonical Policy A fixtures, and the machine-readable schema
for LogiMind, overseen by **TV2 (Data & Test Dataset)**. The authoritative field
definitions are in [`docs/data-dictionary.md`](../docs/data-dictionary.md);
Policy A is described in [`docs/mathematical-model.md`](../docs/mathematical-model.md).

## Directory structure

```text
data/
├── README.md
├── legacy/
│   └── benchmark_data.json     # Legacy prototype input (not Policy A)
├── samples/                    # Ten canonical Policy A fixtures
│   ├── sample_small.json
│   ├── sample_medium.json
│   ├── sample_large.json
│   ├── sample_infeasible.json
│   ├── edge_tight_capacity.json
│   ├── edge_tight_inventory.json
│   ├── edge_equal_costs.json
│   ├── edge_zero_stock.json
│   ├── edge_unavailable_route.json
│   └── edge_infeasible_stock.json
└── schema/
    └── dataset.schema.json     # JSON Schema Draft 2020-12
```

`data/raw/` and `data/processed/` are local scratch areas and are ignored by Git
(see `.gitignore`). They may be created locally but are never committed.

`data/legacy/` is deliberately separate from `data/samples/`: every file in
`samples/` must validate against the canonical Policy A schema, and the legacy
prototype fixture does not.

## Dataset catalogue

| File | Dimensions (warehouses / orders / SKUs) | Expected status | Purpose |
| :--- | :--- | :--- | :--- |
| `samples/sample_small.json` | 2 / 3 / 2 | `FEASIBLE` | Hand-reviewable baseline; demonstrates the contract. |
| `samples/sample_medium.json` | 4 / 20 / 5 | `FEASIBLE` | Generated benchmark with seed `20261111`. |
| `samples/sample_large.json` | 8 / 60 / 10 | `FEASIBLE` | Generated benchmark with seed `20261112`. |
| `samples/sample_infeasible.json` | 2 / 3 / 1 | `INFEASIBLE` | Total capacity is 2 for 3 orders. |
| `samples/edge_tight_capacity.json` | 2 / 3 / 1 | `FEASIBLE` | Total capacity equals order count exactly. |
| `samples/edge_tight_inventory.json` | 2 / 2 / 2 | `FEASIBLE` | SKU-A demand exactly equals available stock. |
| `samples/edge_equal_costs.json` | 2 / 2 / 1 | `FEASIBLE` | Equal shipping costs create multiple optima. |
| `samples/edge_zero_stock.json` | 2 / 2 / 2 | `FEASIBLE` | A warehouse has explicit zero stock; another serves the order. |
| `samples/edge_unavailable_route.json` | 2 / 2 / 1 | `FEASIBLE` | One order–warehouse route is omitted from `shipping_costs`. |
| `samples/edge_infeasible_stock.json` | 2 / 1 / 1 | `INFEASIBLE` | Order demand (50) exceeds every warehouse's stock (10). |
| `legacy/benchmark_data.json` | 3 warehouses / 2 orders | Legacy | Input for `scripts/validate_orders.py`; **not** Policy A. See [Appendix A](../docs/data-dictionary.md#appendix-a-legacy-prototype-dataset-specification). |

`INFEASIBLE` means mathematically infeasible under Policy A, not structurally
invalid. All ten files in `samples/` pass schema and semantic validation. The
legacy fixture is intentionally outside that directory and must not be used as
solver or API input.

## Validate fixtures

From the repository root:

```bash
pip install jsonschema        # required by the validator

python scripts/validate_dataset.py data/samples/
```

Expected: ten `[PASS]` lines, `10 datasets validated.`, `0 validation errors.`,
and exit code `0`.

## Check feasibility

```bash
python scripts/check_feasibility.py data/samples/sample_small.json
python scripts/check_feasibility.py data/samples/sample_infeasible.json
python scripts/check_feasibility.py data/samples/edge_infeasible_stock.json
python scripts/check_feasibility.py data/samples/edge_tight_capacity.json --json
```

`check_feasibility.py` is an exhaustive small-instance oracle. It can return
`UNKNOWN` when its search-state limit is reached; that must never be reported as
infeasibility. Medium and large optimization is TV3's responsibility.

### Verified allocation for `sample_small.json`

The oracle finds the following complete allocation:

| Order | Warehouse |
| :--- | :--- |
| `ORD-001` | `WH-01` |
| `ORD-002` | `WH-01` |
| `ORD-003` | `WH-02` |

Total shipping cost: `12.0`. This is a verified feasible allocation, not a proof
of optimality; optimality certification is TV3's responsibility.

## Generate a reproducible benchmark

```bash
python scripts/generate_dataset.py \
  --warehouses 4 --orders 20 --skus 5 --seed 20261111 \
  --output data/samples/generated.json
```

The generator uses only the Python standard library plus the local validator. It
constructs stock and capacity from a known complete assignment, so generated
datasets are feasible by construction. The same arguments and seed produce
byte-identical JSON on the same Python version. Remove temporary generated files
after local experiments unless they are intended to become reviewed fixtures.

The committed `sample_medium.json` and `sample_large.json` are reproducible
byte-for-byte from seeds `20261111` (4 / 20 / 5) and `20261112` (8 / 60 / 10) when
the same `--dataset-id`, `--name`, and `--description` strings are passed.

## Legacy prototype

```bash
python scripts/validate_orders.py
```

The script resolves `data/legacy/benchmark_data.json` relative to the repository
and prints a Vietnamese allocation log. It is a nearest-warehouse demonstration,
not Policy A.

## Tracking rules

- Commit only curated, reproducible fixtures under `data/samples/`; they must
  validate against the canonical schema.
- Keep genuinely legacy or non-Policy-A inputs under `data/legacy/` and document
  them as such.
- Put machine-readable schemas under `data/schema/`.
- Keep large/generated datasets in `data/raw/` or `data/processed/` locally.
- Never commit SQLite databases (`*.db`, `*.sqlite`, `*.sqlite3`), secrets, or
  extracted customer data.
- Record provenance (generator, seed, or source) in each fixture or in this
  README when adding a new dataset.
- Add edge cases deliberately; do not label a fixture feasible or infeasible
  without verification.
- Add every new canonical fixture to the catalogue above and to the expected
  status table in `tests/test_datasets.py`.
