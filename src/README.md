# Source Code Directory: `src/`

Reserved for the Python application package. **No package source exists yet.**
The legacy prototype is intentionally kept out of this directory at
[`scripts/validate_orders.py`](../scripts/validate_orders.py).

## Intended layout

```text
src/
└── logimind/
    ├── __init__.py
    ├── algorithms/        # TV3: baseline heuristics, MILP model, solver adapter, metrics
    ├── backend/           # TV5: FastAPI application, routes, services, configuration
    └── data/              # TV2/TV5: schema models, dataset loaders, persistence helpers
```

The React + Vite frontend is a separate application under `frontend/`. It must
not be placed inside the Python package.

## Rules for implementation

1. **Create the package only when real code is added.** Do not commit empty
   `__init__.py` files, fake modules, or placeholder services.
2. **Dependencies:** add a `pyproject.toml` when the package needs packaging,
   runtime dependencies, or tool configuration. Do not add one for decoration.
3. **Imports:** use absolute imports rooted at `logimind` (for example
   `from logimind.algorithms.baseline import allocate`).
4. **Contracts:** consume the canonical Policy A dataset contract from
   [`docs/data-dictionary.md`](../docs/data-dictionary.md) and the API contract
   from [`docs/api-contract.md`](../docs/api-contract.md). Do not invent field
   names or business rules.
5. **Determinism:** accept fixed seeds and use a documented tie-breaking rule so
   benchmark runs are reproducible.
6. **Testing:** add unit tests under [`tests/unit/`](../tests/README.md) in the
   same pull request as the implementation.

## Current status

`src/` contains only this README. TV3 (algorithms), TV5 (backend), and shared
data-access code are not implemented. See
[`docs/architecture.md`](../docs/architecture.md) for the proposed component map.
