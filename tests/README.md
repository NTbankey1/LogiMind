# Test Suite: `tests/`

Automated tests for LogiMind, maintained by **TV6** with the module owners.
**No automated test suite exists yet**; this directory currently contains only
this README. Do not claim test coverage for planned components.

## Intended layout

```text
tests/
├── unit/           # Fast, isolated tests (algorithms, validation, persistence)
├── integration/    # API + database + solver interactions
└── e2e/            # End-to-end benchmark and invariant scenarios
```

Create subdirectories only when they contain real tests. The test methodology,
invariants, and required edge cases are defined in
[`docs/testing-strategy.md`](../docs/testing-strategy.md) and
[`docs/project-management/test-plan.md`](../docs/project-management/test-plan.md).

## Running tests (once they exist)

From the repository root:

```bash
python -m pytest tests/ -v
```

`pytest` is not a current dependency because there are no tests yet. When the
first test suite is added, add the test dependency and a `pyproject.toml`
configuration in the same pull request.

## Rules

- A test may only assert behavior that an actual implementation provides.
- Use curated fixtures from `data/samples/`; do not invent hidden test data.
- For optimization tests, assert validity invariants (one warehouse per order,
  per-SKU stock, order-count capacity, total cost recomputation) and objective
  values rather than one arbitrary optimal assignment.
- Distinguish a mathematically infeasible instance from invalid input; they are
  different failure modes.
- Keep tests deterministic: fixed seeds and a documented tie-breaking rule.
- Do not commit generated test output, caches, or databases.

## Current verification

Until an automated suite exists, CI performs repository-hygiene checks: JSON
syntax for `data/samples/*.json`, internal Markdown links, essential-file
presence, and a smoke run of the legacy prototype. See
[`.github/workflows/ci.yml`](../.github/workflows/ci.yml).
