# Test Suite: `tests/`

TV2 automated tests for the Policy A dataset contract, generator, validator, and
feasibility oracle. The suite uses the Python standard library `unittest` and is
also collectable by `pytest`. TV3/TV5/TV6 tests are still planned.

## Current suite

| File | Tests | Scope |
| :--- | ---: | :--- |
| [`test_datasets.py`](test_datasets.py) | 60 | Schema/semantic validation, generator determinism and feasibility, exhaustive feasibility statuses, repository regressions. |

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

| Class | Coverage |
| :--- | :--- |
| `TestDatasetSchemaAndValidation` | Small/medium/large fixtures pass; missing required fields; unknown fields at root and nested; duplicate IDs; duplicate JSON object keys; unknown SKU/warehouse references; incomplete inventory; negative stock/capacity/cost; `NaN`/`Infinity`; boolean rejection; zero cost and zero stock; omitted routes; unsupported schema version; Policy B rejection; all committed fixtures structurally valid. |
| `TestDatasetGenerator` | Determinism across calls and CLI runs (byte-identical); different seeds differ; generated dataset validates; generated dataset is feasible; invalid arguments rejected; written file is valid JSON; feasibility across several seeds. |
| `TestFeasibilityChecker` | Every committed fixture matches its declared status; tight-capacity, tight-inventory, equal-cost, zero-stock, and unavailable-route fixtures are feasible; capacity- and stock-infeasible fixtures are infeasible; state limit returns `UNKNOWN` (not `INFEASIBLE`); invalid and missing input return `INVALID`; input is not mutated; returned assignments satisfy capacity, stock, route, and cost invariants. |
| `TestRepositoryRegression` | Legacy `data/legacy/benchmark_data.json` and `scripts/validate_orders.py` remain present and untouched. |

Expected fixture statuses are asserted in
`TestFeasibilityChecker.test_all_fixtures_match_declared_feasibility_status`, so a
new fixture must be added to that table and to the catalogue in
[`data/README.md`](../data/README.md).

## Planned broader layout

When TV3/TV5/TV6 add tests, use:

```text
tests/
├── unit/           # Fast, isolated tests (algorithms, validation, persistence)
├── integration/    # API + database + solver interactions
└── e2e/            # End-to-end benchmark and invariant scenarios
```

Create subdirectories only when they contain real tests. The methodology,
invariants, and required edge cases are in
[`docs/testing-strategy.md`](../docs/testing-strategy.md) and
[`docs/project-management/test-plan.md`](../docs/project-management/test-plan.md).

## Interpreting results

- `OK` with exit code `0`: all tests passed.
- `FAILED`/`ERROR` with a non-zero exit code: a contract, generator, or
  feasibility invariant regressed. The assertion message names the fixture or
  field involved.
- A feasibility test expecting `INFEASIBLE` must never accept `UNKNOWN`. A
  search-limit result is reported separately and is not proof of infeasibility.
- Tests do not require network access, a database, or a solver.

## Rules

- A test may only assert behavior that an actual implementation provides.
- Use curated fixtures from `data/samples/`; the legacy prototype fixture stays
  in `data/legacy/` and is not part of the Policy A contract.
- For optimization tests, assert validity invariants (one warehouse per order,
  per-SKU stock, order-count capacity, total cost recomputation) and objective
  values rather than one arbitrary optimal assignment.
- Distinguish a mathematically infeasible instance from invalid input.
- Keep tests deterministic: fixed seeds and a documented tie-breaking rule.
- Do not commit generated test output, caches, or databases.

## Current verification and CI

The TV2 job in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) installs
`jsonschema`, validates the ten canonical fixtures, runs this suite, asserts the
expected feasibility status of every fixture, and verifies generator determinism.
The repository-hygiene job also parses JSON fixtures, checks Markdown links,
checks essential files, and smoke-runs the legacy prototype.
