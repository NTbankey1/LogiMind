# Automation Scripts: `scripts/`

Developer utilities, dataset tooling, and the legacy allocation prototype. Run
commands from the repository root unless noted otherwise.

## 1. `validate_orders.py` (implemented legacy prototype)

The only executable script currently in the repository. It is a
**nearest-warehouse demonstration, not the Policy A optimization engine**.

```bash
python scripts/validate_orders.py
python scripts/validate_orders.py path/to/prototype-data.json
```

- **Default input:** `data/samples/benchmark_data.json`, resolved relative to the
  repository root, so the command works from any working directory.
- **Optional argument:** an alternate prototype dataset path.
- **Dependencies:** Python 3.10+ standard library only.
- **Behavior:** loads warehouses and orders, computes Euclidean distance from
  each order destination to each warehouse, assigns the whole order to the
  nearest warehouse with enough aggregate free capacity, and prints a Vietnamese
  allocation log. Occupancy changes are in memory only; the input file is not
  modified.
- **Exit codes:** `0` on a successful load/run; `1` if the dataset cannot be
  loaded.

The input schema is documented in
[Data Dictionary Appendix A](../docs/data-dictionary.md#appendix-a-legacy-prototype-dataset-specification).
It has no per-SKU inventory, no order–warehouse shipping-cost matrix, and no
order-count capacity semantics.

## 2. Planned dataset tooling (TV2)

These scripts do not exist yet; they are recorded here so future work lands in a
consistent location.

| Planned script | Purpose |
| :--- | :--- |
| `generate_dataset.py` | Deterministic, feasible-by-construction Policy A benchmark generator. |
| `validate_dataset.py` | Validate fixtures against the canonical Policy A schema and semantic rules. |
| `check_feasibility.py` | Exhaustive feasibility oracle for small Policy A instances. |

They will require a Python dependency manifest when implemented. Until then, do
not add placeholder files or an empty `pyproject.toml`.

## 3. Conventions

- Python files use `snake_case.py`.
- Scripts must not depend on the current working directory for bundled data;
  resolve paths relative to `__file__` or accept an explicit argument.
- Do not commit generated datasets to `scripts/`; write them to `data/samples/`
  only after review.
- Do not place experimental one-off scripts in the repository root.
