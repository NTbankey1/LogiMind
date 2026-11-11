# LogiMind Dataset Fixtures

This directory contains versioned, tracked JSON fixtures used by TV2, TV3 and TV6. The canonical contract is [`docs/data-dictionary.md`](../docs/data-dictionary.md), with machine-readable JSON Schema at [`schema/dataset.schema.json`](schema/dataset.schema.json).

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

All files in `samples/` are intentionally committed because they are reproducible benchmark inputs. Do not commit local databases, raw customer data, generated scratch files, or runtime outputs here.

## Dataset catalogue

| File | Intended result / coverage |
|---|---|
| `sample_small.json` | Feasible, hand-reviewable; 2 warehouses, 3 orders, 2 SKUs. |
| `sample_medium.json` | Feasible generated benchmark; 4 warehouses, 20 orders, 5 SKUs. |
| `sample_large.json` | Feasible generated benchmark; 8 warehouses, 60 orders, 10 SKUs. |
| `sample_infeasible.json` | Infeasible: 3 orders but only 2 total order-capacity slots. |
| `edge_tight_capacity.json` | Feasible with every warehouse capacity slot consumed. |
| `edge_tight_inventory.json` | Feasible with SKU demand exactly equal to available stock. |
| `edge_equal_costs.json` | Feasible tie: two warehouses have equal shipping costs. |
| `edge_zero_stock.json` | A warehouse has explicit zero stock; an alternate warehouse serves the order. |
| `edge_unavailable_route.json` | One order–warehouse route is absent from its cost map. |
| `edge_infeasible_stock.json` | Infeasible: order demand exceeds every warehouse's available stock. |

## Validate fixtures

From the repository root:

```bash
python scripts/validate_dataset.py data/samples
python -m unittest discover -s tests -v
python scripts/check_feasibility.py data/samples/sample_small.json
python scripts/check_feasibility.py data/samples/sample_infeasible.json
```

`check_feasibility.py` is an exhaustive small-instance oracle. It can return `UNKNOWN` when its search-state limit is reached; that must not be reported as infeasibility.

## Generate a reproducible benchmark

```bash
python scripts/generate_dataset.py \
  --warehouses 4 --orders 20 --skus 5 --seed 20261111 \
  --output data/samples/generated.json
```

The generator uses only the Python standard library and a fixed seed. It constructs stock and capacity from a known complete assignment, so a generated dataset is feasible by construction. Remove temporary generated files after local experiments unless they are intended to become reviewed fixtures.
