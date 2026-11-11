# Test Suite: `tests/`

TV2 automated tests for the Policy A dataset contract, generator, validator, and
feasibility oracle. The suite uses the Python standard library `unittest` and is
also collectable by `pytest`.

## Prerequisites

- Python 3.10 or newer.
- `jsonschema` (required by `scripts/validate_dataset.py`).
- `pytest` only if you choose the pytest runner.

```bash
pip install jsonschema pytest
# or
pip install -e ".[dev]"
```

## Running the tests

From the repository root:

```bash
# Standard library runner (used by CI)
python -m unittest discover -s tests -v

# pytest (optional)
python -m pytest tests/ -v
```

Running `python -m unittest` from other directories may break the `scripts`
imports; run from the repository root.

## What the suite covers

`tests/test_datasets.py` contains four test classes:

| Class | Coverage |
| :--- | :--- |
| `TestDatasetSchemaAndValidation` | Small/medium/large fixtures pass; missing required fields; unknown fields at root and nested; duplicate IDs; duplicate JSON object keys; unknown SKU/warehouse references; incomplete inventory; negative stock/capacity/cost; `NaN`/`Infinity`; boolean rejection; zero cost and zero stock; omitted routes; unsupported schema version; Policy B rejection; all committed fixtures structurally valid. |
| `TestDatasetGenerator` | Determinism across calls and across CLI runs (byte-identical); different seeds differ; generated dataset validates; generated dataset is feasible; invalid arguments rejected; written file is valid JSON; feasibility across several seeds. |
| `TestFeasibilityChecker` | Every committed fixture matches its declared status; tight-capacity, tight-inventory, equal-cost, zero-stock, and unavailable-route fixtures are feasible; capacity- and stock-infeasible fixtures are infeasible; state limit returns `UNKNOWN` (not `INFEASIBLE`); invalid and missing input return `INVALID`; input is not mutated; returned assignments satisfy capacity, stock, route, and cost invariants. |
| `TestRepositoryRegression` | Legacy `benchmark_data.json` and `validate_orders.py` remain present and untouched. |

Expected fixture statuses are asserted in
`TestFeasibilityChecker.test_all_fixtures_match_declared_feasibility_status`, so a
new fixture must be added to that table and to the catalogue in
[`data/README.md`](../data/README.md).

## Interpreting results

- `OK` with exit code `0`: all tests passed.
- `FAILED`/`ERROR` with a non-zero exit code: a contract, generator, or
  feasibility invariant regressed. The assertion message names the fixture or
  field involved.
- A feasibility test expecting `INFEASIBLE` must never accept `UNKNOWN`. A
  search-limit result is reported separately and is not proof of infeasibility.
- Tests do not require network access, a database, or a solver.

## Adding tests

- Keep fixtures deterministic and schema-valid.
- For datasets with multiple optimal allocations, assert invariants and objective
  values rather than one arbitrary warehouse choice.
- When adding a validation rule, add both a failing case and a passing case.
