# LogiMind Dataset Fixtures

This directory contains the tracked Policy A dataset contract, schema, and
benchmark fixtures used by TV2, TV3, TV5, and TV6.

- Canonical human-readable contract: [`docs/data-dictionary.md`](../docs/data-dictionary.md)
- Machine-readable schema: [`schema/dataset.schema.json`](schema/dataset.schema.json)
- Policy decision: [`docs/decisions/0004-allocation-policy-a.md`](../docs/decisions/0004-allocation-policy-a.md)
- Tooling documentation: [`scripts/README.md`](../scripts/README.md)

## Tracked structure

```text
data/
├── README.md
├── schema/
│   └── dataset.schema.json
└── samples/
    ├── sample_small.json
    ├── sample_medium.json
    ├── sample_large.json
    ├── sample_infeasible.json
    ├── edge_tight_capacity.json
    ├── edge_tight_inventory.json
    ├── edge_equal_costs.json
    ├── edge_zero_stock.json
    ├── edge_unavailable_route.json
    └── edge_infeasible_stock.json
```

All files in `samples/` are intentionally committed because they are reproducible
benchmark inputs. Do not commit local databases, raw customer data, generated
scratch files, or runtime outputs here. A generated file is only committed after
it is reviewed, validated, and checked for feasibility.

## Dataset catalogue

| File | Dimensions (warehouses / orders / SKUs) | Expected status | Purpose |
| :--- | :--- | :--- | :--- |
| `sample_small.json` | 2 / 3 / 2 | `FEASIBLE` | Hand-reviewable baseline; demonstrates the contract. |
| `sample_medium.json` | 4 / 20 / 5 | `FEASIBLE` | Generated benchmark with seed `20261111`. |
| `sample_large.json` | 8 / 60 / 10 | `FEASIBLE` | Generated benchmark with seed `20261112`. |
| `sample_infeasible.json` | 2 / 3 / 1 | `INFEASIBLE` | Total capacity is 2 for 3 orders. |
| `edge_tight_capacity.json` | 2 / 3 / 1 | `FEASIBLE` | Total capacity equals order count exactly. |
| `edge_tight_inventory.json` | 2 / 2 / 2 | `FEASIBLE` | SKU-A demand exactly equals available stock. |
| `edge_equal_costs.json` | 2 / 2 / 1 | `FEASIBLE` | Equal shipping costs create multiple optima. |
| `edge_zero_stock.json` | 2 / 2 / 2 | `FEASIBLE` | A warehouse has explicit zero stock; another serves the order. |
| `edge_unavailable_route.json` | 2 / 2 / 1 | `FEASIBLE` | One order–warehouse route is omitted from `shipping_costs`. |
| `edge_infeasible_stock.json` | 2 / 1 / 1 | `INFEASIBLE` | Order demand (50) exceeds every warehouse's stock (10). |

`INFEASIBLE` means mathematically infeasible under Policy A, not structurally
invalid. All ten files pass schema and semantic validation.

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

## Adding a fixture

1. Generate or hand-build the dataset following `docs/data-dictionary.md`.
2. Run `validate_dataset.py` and `check_feasibility.py`.
3. Add the file to the catalogue above.
4. Add its expected status to
   `tests/test_datasets.py::test_all_fixtures_match_declared_feasibility_status`.
5. Document any controlled infeasibility reason in the dataset `description`.
