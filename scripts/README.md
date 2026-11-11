# Automation Scripts: `scripts/`

Developer utilities, dataset tooling, and the legacy allocation prototype. The
canonical dataset contract is
[`docs/data-dictionary.md`](../docs/data-dictionary.md), with the machine-readable
schema at [`data/schema/dataset.schema.json`](../data/schema/dataset.schema.json).

| Script | Purpose |
| :--- | :--- |
| [`validate_orders.py`](validate_orders.py) | Legacy nearest-warehouse prototype (not Policy A). |
| [`validate_dataset.py`](validate_dataset.py) | Structural JSON Schema validation plus Policy A cross-record checks. |
| [`generate_dataset.py`](generate_dataset.py) | Deterministic, feasible-by-construction Policy A dataset generator. |
| [`check_feasibility.py`](check_feasibility.py) | Exhaustive small-instance feasibility oracle. |

## Dependencies

`validate_orders.py` uses only the Python standard library. The three TV2 tools
require **`jsonschema`** (JSON Schema Draft 2020-12); the generator and checker
import the validator.

```bash
# Python 3.10 or newer
pip install jsonschema
# or install the repository extras
pip install -e ".[dev]"
```

---

## 1. `validate_orders.py` (legacy prototype)

A **nearest-warehouse demonstration, not the Policy A optimization engine**.

```bash
python scripts/validate_orders.py
python scripts/validate_orders.py path/to/prototype-data.json
```

- **Default input:** `data/legacy/benchmark_data.json`, resolved relative to the
  repository root, so the command works from any working directory.
- **Optional argument:** an alternate prototype dataset path.
- **Behavior:** computes Euclidean distance from each order destination to each
  warehouse, assigns the whole order to the nearest warehouse with enough
  aggregate free capacity, and prints a Vietnamese allocation log. Occupancy
  changes are in memory only; the input file is not modified.
- **Exit codes:** `0` on a successful load/run; `1` if the dataset cannot load.

The input schema is documented in
[Data Dictionary Appendix A](../docs/data-dictionary.md#appendix-a-legacy-prototype-dataset-specification).
It has no per-SKU inventory, no precomputed order–warehouse shipping-cost matrix,
and no Policy A order-count capacity semantics.

---

## 2. `validate_dataset.py`

Validates a file or every `*.json` file directly inside a directory.

```bash
python scripts/validate_dataset.py data/samples/
python scripts/validate_dataset.py data/samples/sample_small.json
python scripts/validate_dataset.py FILE --schema path/to/schema.json
```

Checks performed:

- JSON syntax and duplicate object keys.
- JSON Schema Draft 2020-12 conformance (`additionalProperties: false` at every
  entity level).
- Unique `sku_id`, `warehouse_id`, and `order_id` values.
- Complete inventory for every warehouse and every SKU.
- Known SKU references in `items` and known warehouse references in
  `shipping_costs`.
- Positive integer quantities, non-negative integer stock/capacity, and finite
  non-negative shipping costs.
- Boolean rejection in integer/number fields.
- Policy A conformance; Policy B fields are rejected.

Exit codes: `0` when all files are structurally valid; `1` on any validation
failure or an unreadable schema/path. Feasibility is not assessed here.

Importable API:

```python
from pathlib import Path
from scripts.validate_dataset import validate_dataset_data, validate_file

is_valid, errors = validate_file(Path("data/samples/sample_small.json"))
```

`validate_dataset_data(dataset_dict, schema=None)` validates an already-parsed
dictionary and is used by the generator and feasibility checker.

---

## 3. `generate_dataset.py`

Generates a deterministic Policy A dataset that is **feasible by construction**.

```bash
python scripts/generate_dataset.py \
  --warehouses 4 --orders 20 --skus 5 --seed 20261111 \
  --output data/samples/generated.json
```

| Argument | Required | Meaning |
| :--- | :--- | :--- |
| `--warehouses` | Yes | Number of warehouses, integer `>= 1`. |
| `--orders` | Yes | Number of orders, integer `>= 1`. |
| `--skus` | Yes | Number of SKUs, integer `>= 1`. |
| `--seed` | Yes | Seed for Python's `random.Random(seed)`. |
| `--output` | Yes | Output JSON path; parent directories are created. |
| `--dataset-id` | No | Overrides the generated `dataset_id`. |
| `--name` | No | Overrides the generated dataset name. |
| `--description` | No | Overrides the generated description. |

The same arguments and seed produce byte-identical JSON on the same Python
version. Metadata records the generator name and seed. The command validates the
dataset in memory, writes it, then re-reads and validates the file on disk.

Exit codes: `0` on success; `1` for invalid arguments, validation failure, or a
filesystem write error.

---

## 4. `check_feasibility.py`

Deterministic exhaustive search for small Policy A instances.

```bash
python scripts/check_feasibility.py data/samples/sample_small.json
python scripts/check_feasibility.py data/samples/sample_infeasible.json --json
python scripts/check_feasibility.py FILE --max-states 100000
```

| Argument | Required | Meaning |
| :--- | :--- | :--- |
| `target` | Yes | Dataset JSON file. |
| `--json` | No | Machine-readable result object. |
| `--max-states` | No | Search-state limit; default `500000`. |

The checker validates the dataset, applies necessary conditions (total capacity,
per-SKU stock, per-order fulfillability), then runs depth-first backtracking with
inventory/capacity deducted incrementally. The input dictionary is never mutated.

| Status | Meaning |
| :--- | :--- |
| `FEASIBLE` | A complete allocation was found; assignment and cost returned. |
| `INFEASIBLE` | Search exhausted, or a proven necessary condition failed. |
| `UNKNOWN` | `--max-states` reached before proof. **Never** treat as infeasible. |
| `INVALID` | Input failed dataset validation or could not be parsed. |

Exit codes: `0` for `FEASIBLE` or `INFEASIBLE`; `1` for `INVALID`; `2` for
`UNKNOWN`.

Limitation: exhaustive search is exponential and intended for small fixtures. It
verifies existence, not optimality, and does not replace TV3's MILP solver on
medium and large datasets.

---

## 5. Conventions

- Python files use `snake_case.py`.
- Scripts must not depend on the current working directory for bundled data;
  resolve paths relative to `__file__` or accept an explicit argument.
- Do not commit generated datasets to `scripts/`; write them to `data/samples/`
  only after review.
- Do not place experimental one-off scripts in the repository root.
