# Test Suite Directory: `tests/`

This directory houses automated test suites for the LogiMind project, maintained by **TV6** in collaboration with all module leads.

---

## 1. Planned Test Structure

```text
tests/
├── conftest.py             # Shared pytest fixtures, sample problem factories
├── unit/                   # Fast, isolated unit tests
│   ├── test_baseline.py    # Test baseline heuristic logic (TV3)
│   ├── test_milp.py        # Test MILP solver mathematical validity (TV3)
│   └── test_schemas.py     # Test Pydantic model validation (TV5)
├── integration/            # Component interaction tests
│   ├── test_api.py         # Test backend endpoints against SQLite (TV5 & TV6)
│   └── test_solver_api.py  # Test backend calling solver wrapper (TV5 & TV3)
└── e2e/                    # End-to-end benchmark scenarios
    ├── test_invariants.py  # Mathematical invariant assertion across all runs (TV6)
    └── test_benchmarks.py  # Performance & cost reduction verification (TV6)
```

---

## 2. Test Execution Guidelines

Once Python dependencies are established:
```bash
# Execute entire test suite
pytest tests/ -v

# Run with test coverage report
pytest --cov=src tests/
```

See [docs/testing-strategy.md](../docs/testing-strategy.md) for testing invariants and edge-case requirements.
