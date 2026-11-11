# LogiMind

LogiMind is an academic software-engineering project for the **Multi-Warehouse
Order Allocation Problem (MWOAP)**: assigning each customer order to exactly one
fulfillment warehouse while respecting per-SKU stock and order-count capacity,
then comparing a simple heuristic with a Mixed-Integer Linear Programming (MILP)
allocation.

The repository is at the **documentation + data-contract + prototype stage**. A
standalone legacy allocation prototype is executable. The Policy A data contract
is owned by TV2 and still being finalized; the solver, FastAPI backend, SQLite
persistence, React frontend, and automated test suite are planned but not
implemented.

---

## 1. Project status

| Area | Status | Evidence |
| :--- | :--- | :--- |
| Formal requirements and mathematical model | **Present; Policy A selected** | [requirements](docs/requirements.md), [mathematical model](docs/mathematical-model.md) |
| Data dictionary | **Draft** | [docs/data-dictionary.md](docs/data-dictionary.md) (includes the legacy prototype appendix) |
| Curated fixtures | **Present** | [`data/samples/benchmark_data.json`](data/samples/benchmark_data.json), [`data/samples/sample_small.json`](data/samples/sample_small.json) |
| Legacy allocation prototype | **Implemented; not Policy A** | [`scripts/validate_orders.py`](scripts/validate_orders.py) (Python standard library) |
| Architecture and API contract | **Proposed** | [architecture](docs/architecture.md), [API contract](docs/api-contract.md) |
| ADR-001/002/003 (solver, backend, database) | **Proposed** | [decisions](docs/decisions/README.md) |
| Optimization engine (`src/logimind/`) | **Not started** | No package source; see the intended layout in [src/README.md](src/README.md) |
| Backend and SQLite | **Not started** | No backend source or migrations |
| Frontend | **Not started** | No frontend application or package manifest |
| Automated tests | **Not started** | `tests/` contains only a planning README |
| CI | **Repository hygiene + prototype smoke** | [.github/workflows/ci.yml](.github/workflows/ci.yml) |

### Allocation policy

The Project Lead selected **Policy A**:

- every order is assigned to exactly one warehouse;
- split shipments are not allowed;
- all orders must be fulfilled completely;
- warehouse capacity is measured in **number of orders**;
- inventory is tracked **per SKU**;
- the objective is to minimize total shipping cost;
- there is no unassigned-order penalty.

If no complete allocation exists, the instance is infeasible. The authoritative
formulation is [docs/mathematical-model.md](docs/mathematical-model.md); the data
contract is [docs/data-dictionary.md](docs/data-dictionary.md).

### Legacy prototype (not Policy A)

[`scripts/validate_orders.py`](scripts/validate_orders.py) loads
[`data/samples/benchmark_data.json`](data/samples/benchmark_data.json), computes
Euclidean distances, and assigns each whole order to the nearest warehouse with
enough aggregate free capacity. It has no per-SKU inventory, no precomputed
shipping-cost matrix, and no Policy A capacity semantics. It is a demonstration,
not the optimization engine.

---

## 2. Architecture

### Implemented today

```text
data/samples/benchmark_data.json  ->  scripts/validate_orders.py  ->  console output
(legacy prototype input)              (nearest-warehouse heuristic)
```

### Planned architecture (not implemented)

```text
React + Vite frontend (frontend/)
        |  HTTP (proposed API contract)
        v
FastAPI backend (src/logimind/backend/)  <-->  SQLite
        |
        v
Optimization engine (src/logimind/algorithms/): baseline + MILP
        ^
        |
data/samples/ + data/schema/ + tests/
```

Technology choices remain **proposed** in ADR-001 (PuLP/CBC), ADR-002 (FastAPI),
and ADR-003 (SQLite). The detailed component map and data flow are in
[docs/architecture.md](docs/architecture.md).

---

## 3. Repository structure

```text
LogiMind/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/ci.yml
│   └── pull_request_template.md
├── data/
│   ├── README.md
│   └── samples/
│       ├── benchmark_data.json     # Legacy prototype fixture (not Policy A)
│       └── sample_small.json       # Draft toy fixture
├── docs/
│   ├── decisions/                  # ADR index and ADR-001..003
│   ├── project-management/         # Status, tracker, plans, cleanup record
│   ├── reference/
│   │   └── project-analysis.docx   # Original academic analysis
│   ├── api-contract.md
│   ├── architecture.md
│   ├── data-dictionary.md
│   ├── git-workflow.md
│   ├── index.md
│   ├── integration-guide.md
│   ├── mathematical-model.md
│   ├── project-overview.md
│   ├── requirements.md
│   ├── team-responsibilities.md
│   └── testing-strategy.md
├── scripts/
│   ├── README.md
│   └── validate_orders.py          # Legacy allocation prototype
├── src/
│   └── README.md                   # Intended src/logimind/ package layout
├── tests/
│   └── README.md                   # Intended unit/integration/e2e layout
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CLAUDE.md
├── CONTRIBUTING.md
└── README.md
```

There is no `pyproject.toml` yet. The prototype uses only the standard library;
a dependency/packaging manifest will be added when the `src/logimind/` package
and automated tests exist. Empty package, frontend, and test directories are
intentionally not created in advance.

---

## 4. Installation and setup

### Requirements

- **Python 3.10 or newer** (CI uses Python 3.10)
- **Git**
- No third-party Python packages are required by the current prototype.

```bash
git clone https://github.com/NTbankey1/LogiMind.git
cd LogiMind
python3 --version          # confirm 3.10+
```

No virtual environment is strictly required for the standard-library prototype,
but one is recommended for future work:

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

[.env.example](.env.example) documents proposed backend/solver settings; copy it
to `.env` only when those components exist. `.env` is ignored by Git.

---

## 5. Running and testing

### Run the legacy prototype

From any directory:

```bash
python scripts/validate_orders.py
```

The script resolves its default input relative to the repository, so it no
longer depends on the current working directory. An alternate prototype file can
be supplied:

```bash
python scripts/validate_orders.py path/to/prototype-data.json
```

It prints a Vietnamese allocation log and does not modify the input file. It is
not the Policy A optimizer.

### Validate curated JSON fixtures

```bash
python -m json.tool data/samples/benchmark_data.json > /dev/null
python -m json.tool data/samples/sample_small.json > /dev/null
```

### Automated tests

There is currently **no automated test suite**. `tests/` contains only a planning
README, and the CI workflow does not run `pytest`. Do not report test coverage
for components that do not exist. The planned layout is described in
[tests/README.md](tests/README.md).

### CI checks

[.github/workflows/ci.yml](.github/workflows/ci.yml) verifies:

- every JSON file under `data/samples/` parses;
- every internal Markdown link resolves;
- essential repository files exist;
- the legacy prototype still runs successfully.

---

## 6. Team responsibilities

Roles follow [docs/team-responsibilities.md](docs/team-responsibilities.md).
Assignee names, GitHub handles, and deadlines remain **TBD**.

| Role | Scope | Current repository evidence |
| :--- | :--- | :--- |
| **TV1** | Business analysis and mathematical modeling | Policy A model and requirements are present |
| **TV2** | Data and test datasets | Draft data dictionary and fixtures; canonical Policy A schema and fixtures pending |
| **TV3** | Optimization algorithms | Not started; intended under `src/logimind/algorithms/` |
| **TV4** | Frontend | Not started; intended under `frontend/` |
| **TV5** | Backend and database | Not started; intended under `src/logimind/backend/` |
| **TV6** | Integration, testing, reporting | CI hygiene exists; automated test suite not started |

---

## 7. Known limitations and open decisions

- The legacy prototype and `benchmark_data.json` use an older flat schema with
  aggregate capacity and Euclidean costs. They are documented in Appendix A of
  the data dictionary and are not valid Policy A solver input.
- `data/samples/sample_small.json` is a draft scaffold fixture and still contains
  pre-Policy-A fields (split/unassigned penalties, `daily_capacity`,
  `handling_cost_per_unit`). TV2 owns its replacement.
- The canonical Policy A JSON Schema, generator, validator, and feasibility
  checker are not in this branch; TV2 is responsible for them.
- `docs/data-dictionary.md` still describes a **proposed relational storage
  schema**; it is not the canonical benchmark contract. Fields outside the
  Policy A objective are flagged there.
- No solver, backend, database, frontend, or automated test suite exists.
- ADR-001, ADR-002, and ADR-003 remain `PROPOSED`.
- `pyproject.toml` is intentionally deferred until there is actual Python
  package/test code to configure.

---

## 8. Documentation map

| Document | Contents |
| :--- | :--- |
| [docs/index.md](docs/index.md) | Documentation centre and role-based reading paths |
| [docs/project-overview.md](docs/project-overview.md) | Problem context, objectives, scope |
| [docs/requirements.md](docs/requirements.md) | Business requirements and acceptance tests |
| [docs/mathematical-model.md](docs/mathematical-model.md) | Policy A formulation and worked examples |
| [docs/data-dictionary.md](docs/data-dictionary.md) | Proposed storage schema + legacy prototype Appendix A |
| [data/README.md](data/README.md) | Dataset tracking policy and fixture catalogue |
| [scripts/README.md](scripts/README.md) | Prototype usage and planned utilities |
| [src/README.md](src/README.md) | Intended Python package layout |
| [tests/README.md](tests/README.md) | Intended test layout and execution rules |
| [docs/architecture.md](docs/architecture.md) | Proposed components, paths, and data flow |
| [docs/api-contract.md](docs/api-contract.md) | Proposed REST endpoints and payloads |
| [docs/testing-strategy.md](docs/testing-strategy.md) | Test tiers, invariants, edge cases |
| [docs/integration-guide.md](docs/integration-guide.md) | Module handoff checklists |
| [docs/team-responsibilities.md](docs/team-responsibilities.md) | Role matrix (assignees TBD) |
| [docs/decisions/README.md](docs/decisions/README.md) | ADR index and status definitions |
| [docs/project-management/project-status.md](docs/project-management/project-status.md) | Evidence-based project status |
| [docs/project-management/repository-cleanup-plan.md](docs/project-management/repository-cleanup-plan.md) | Repository audit and cleanup record |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Branch, commit, PR, and review workflow |

---

## 9. Contributing

All changes go through a Pull Request targeting `main`; direct pushes are not
permitted. See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, Conventional
Commits, review requirements, and conflict handling.
