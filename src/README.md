# Source Code Directory: `src/`

This directory is reserved for application, optimization, and service source code for the LogiMind system.

---

## 1. Planned Codebase Organization

Following architecture discussions in [docs/architecture.md](../docs/architecture.md), the proposed internal package layout is:

```text
src/
├── algorithms/           # Managed by TV3 (Optimization Algorithms)
│   ├── __init__.py
│   ├── base.py           # Abstract solver interface (callable contract)
│   ├── baseline.py       # Heuristic solvers (Greedy / Nearest)
│   ├── milp_solver.py    # MILP PuLP / OR-Tools formulation
│   └── metrics.py        # Cost calculation & comparison utilities
├── backend/              # Managed by TV5 (Backend & Database)
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── config.py         # App configuration & environment loader
│   ├── api/              # API route controllers (/health, /allocations)
│   ├── models/           # SQLAlchemy / SQLModel database entities
│   └── services/         # Business logic & solver orchestration
└── frontend/             # Managed by TV4 (Frontend UI)
    ├── package.json      # Frontend package configuration (if React/Vite)
    ├── index.html
    └── src/              # UI components, state management, and visualizations
```

---

## 2. Implementation Rules for Contributors

1. **Adhere to Contracts:** All data exchanges between frontend and backend must strictly conform to [docs/api-contract.md](../docs/api-contract.md).
2. **Encapsulate Algorithms:** The optimization engine must be callable as an isolated Python package without direct coupling to web or HTTP frameworks.
3. **Deterministic Logic:** Always provide fixed seeds or tie-breaking policies to ensure allocation results are reproducible during grading and tests.
