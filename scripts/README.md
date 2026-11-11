# Automation Scripts: `scripts/`

TV2 dataset tooling. The canonical contract is
[`docs/data-dictionary.md`](../docs/data-dictionary.md) and
[`data/schema/dataset.schema.json`](../data/schema/dataset.schema.json).

| Script | Purpose |
| :--- | :--- |
| [`validate_dataset.py`](validate_dataset.py) | Structural JSON Schema validation plus Policy A cross-record checks. |
| [`generate_dataset.py`](generate_dataset.py) | Deterministic, feasible-by-construction dataset generator. |
| [`check_feasibility.py`](check_feasibility.py) | Exhaustive small-instance feasibility oracle. |

## Dependencies

All three scripts use the Python standard library except `validate_dataset.py`,
which requires **`jsonschema`** (JSON Schema Draft 2020-12). The other scripts
import the validator, so the dependency is required for them too.

```bash
# Python 3.10 or newer
pip install jsonschema
# or install the repository extras
pip install -e ".[dev]"
```

No other third-party packages are required by TV2.

---

## 1. `validate_dataset.py`

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

Output:

```text
[PASS] sample_small.json
[PASS] sample_medium.json
...
10 datasets validated.
0 validation errors.
```

Exit codes:

| Code | Meaning |
| :--- | :--- |
| `0` | All files are structurally valid. Feasibility is not assessed. |
| `1` | At least one file failed validation, or the schema/path could not be read. |

Importable API:

```python
from scripts.validate_dataset import validate_dataset_data, validate_file
is_valid, errors = validate_file(Path("data/samples/sample_small.json"))
```

`validate_dataset_data(dataset_dict, schema=None)` validates an already-parsed
dictionary and is used by the generator and feasibility checker.

---

## 2. `generate_dataset.py`

Generates a deterministic Policy A dataset that is **feasible by construction**.

```bash
python scripts/generate_dataset.py \
  --warehouses 4 \
  --orders 20 \
  --skus 5 \
  --seed 20261111 \
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

Reproducibility: the same arguments and seed produce byte-identical JSON on the
same Python version. Metadata records the generator name and seed.

Construction strategy:

1. Create the SKU catalogue and warehouses.
2. Generate positive order demand.
3. Assign each order to a known warehouse internally (round-robin).
4. Set each warehouse's stock and `capacity_orders` from that private assignment,
   adding buffer.
5. Emit a shipping cost for the construction route (and usually other routes).
6. Serialize only the dataset; the construction assignment is not exposed.

The command validates the dataset in memory, writes it, then re-reads and
validates the file on disk before reporting success.

Exit codes: `0` on success; `1` for invalid arguments, validation failure, or a
filesystem write error.

---

## 3. `check_feasibility.py`

Deterministic exhaustive search for small Policy A instances. Useful as an
independent oracle for TV3 and TV6 fixtures.

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

Algorithm: validate the dataset, apply necessary conditions (total capacity,
total per-SKU stock, per-order individual fulfillability), then run depth-first
backtracking. Orders are ordered by fewest candidate warehouses (MRV), ties by
`order_id`; warehouses are tried in sorted ID order. Capacity and inventory are
deducted incrementally and restored on backtrack. The input dictionary is never
mutated.

Statuses:

| Status | Meaning |
| :--- | :--- |
| `FEASIBLE` | A complete allocation was found; assignment and total cost returned. |
| `INFEASIBLE` | The search space was exhausted, or a proven necessary condition failed. |
| `UNKNOWN` | `--max-states` was reached before proof. **Never** treat as infeasible. |
| `INVALID` | The input failed dataset validation or could not be parsed. |

Exit codes:

| Code | Meaning |
| :--- | :--- |
| `0` | The check completed with `FEASIBLE` or `INFEASIBLE` (both are successful proofs). |
| `1` | `INVALID` input. |
| `2` | `UNKNOWN` (search limit reached). |

JSON output example:

```json
{
  "status": "FEASIBLE",
  "states_explored": 4,
  "assignment": {"ORD-001": "WH-01", "ORD-002": "WH-01", "ORD-003": "WH-02"},
  "total_shipping_cost": 12.0
}
```

Limitation: exhaustive search is exponential and intended for small fixtures.
It verifies existence, not optimality, and does not replace TV3's MILP solver on
medium and large datasets.
