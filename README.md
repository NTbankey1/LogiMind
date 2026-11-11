# LogiMind

LogiMind is an academic software-engineering project for the **Multi-Warehouse
Order Allocation Problem (MWOAP)**: assigning each customer order to exactly one
fulfillment warehouse while respecting per-SKU stock and order-count capacity,
then comparing a simple heuristic with a Mixed-Integer Linear Programming (MILP)
allocation.

The repository is at the **data-contract + prototype stage**. TV2's Policy A data
layer is implemented: canonical schema, ten benchmark/edge-case fixtures, a
deterministic generator, a validator, an exhaustive small-instance feasibility
oracle, automated tests, and a CI job. A standalone legacy prototype is also
runnable. The solver, FastAPI backend, SQLite persistence, and React frontend are
planned but not implemented.

---

## 1. Project status

| Area | Status | Evidence |
| :--- | :--- | :--- |
| Allocation policy | **Decided: Policy A** | [ADR-004](docs/decisions/0004-allocation-policy-a.md), [mathematical model](docs/mathematical-model.md) |
| Canonical data contract | **Implemented** | [data dictionary](docs/data-dictionary.md), [dataset.schema.json](data/schema/dataset.schema.json) |
| Benchmark and edge-case fixtures | **Implemented** | Ten fixtures under [data/samples/](data/samples/); catalogue in [data/README.md](data/README.md) |
| Dataset generator | **Implemented** | [scripts/generate_dataset.py](scripts/generate_dataset.py) |
| Dataset validator | **Implemented** | [scripts/validate_dataset.py](scripts/validate_dataset.py) |
| Feasibility oracle (small instances) | **Implemented** | [scripts/check_feasibility.py](scripts/check_feasibility.py) |
| Automated TV2 tests | **Implemented** | [tests/test_datasets.py](tests/test_datasets.py), 60 tests |
| CI | **Hygiene + TV2 dataset/feasibility job** | [.github/workflows/ci.yml](.github/workflows/ci.yml) |
| Requirements and mathematical model | **Present; Policy A canonical** | [requirements](docs/requirements.md), [mathematical model](docs/mathematical-model.md) |
| Architecture and API contract | **Proposed** | [architecture](docs/architecture.md), [API contract](docs/api-contract.md) |
| ADR-001/002/003 (solver, backend, database) | **Proposed** | [decisions](docs/decisions/README.md) |
| Optimization engine (`src/logimind/`) | **Not started** | See the intended layout in [src/README.md](src/README.md) |
| Backend and SQLite | **Not started** | No backend source or migrations |
| Frontend | **Not started** | No frontend application or package manifest |
| Legacy allocation prototype | **Implemented; not Policy A** | [scripts/validate_orders.py](scripts/validate_orders.py) |

### Allocation policy (Policy A)

There is no split shipment and no unassigned-order penalty:

- every order is assigned to exactly one warehouse;
- all orders must be fulfilled completely;
- warehouse capacity is measured in **number of orders**;
- inventory is tracked **per SKU**;
- the objective minimizes total shipping cost;
- if no complete allocation exists, the instance is infeasible.

The authoritative formulation is [docs/mathematical-model.md](docs/mathematical-model.md);
the dataset contract is [docs/data-dictionary.md](docs/data-dictionary.md).

### Legacy prototype (not Policy A)

[`scripts/validate_orders.py`](scripts/validate_orders.py) loads
[`data/legacy/benchmark_data.json`](data/legacy/benchmark_data.json), computes
Euclidean distances, and assigns each whole order to the nearest warehouse with
enough aggregate free capacity. It has no per-SKU inventory, no precomputed
shipping-cost matrix, and no Policy A capacity semantics. It is a demonstration,
not the optimization engine.

---

## 2. Architecture

### Implemented today

```text
data/schema/dataset.schema.json
        |
        v
data/samples/*.json  ->  scripts/validate_dataset.py  ->  PASS / FAIL
        |                        |
        |                        +-> scripts/check_feasibility.py -> status
        v
scripts/generate_dataset.py  ->  new deterministic, feasible dataset

data/legacy/benchmark_data.json  ->  scripts/validate_orders.py  ->  console output
(legacy, non-Policy-A)
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
and ADR-003 (SQLite); ADR-004 (Policy A) is **accepted**. The component map and
data flow are in [docs/architecture.md](docs/architecture.md).

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
│   ├── legacy/benchmark_data.json   # Legacy prototype input (not Policy A)
│   ├── samples/                     # Ten canonical Policy A fixtures
│   └── schema/dataset.schema.json
├── docs/
│   ├── decisions/                   # ADR index, ADR-001..004
│   ├── project-management/          # Status, tracker, plans, cleanup record
│   ├── reference/project-analysis.docx
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
│   ├── validate_orders.py           # Legacy prototype
│   ├── validate_dataset.py
│   ├── generate_dataset.py
│   └── check_feasibility.py
├── src/README.md                    # Intended src/logimind/ package layout
├── tests/
│   ├── README.md
│   └── test_datasets.py
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CLAUDE.md
├── CONTRIBUTING.md
├── README.md
└── pyproject.toml                   # TV2 test/data tooling and dev extras
```

`frontend/` and `src/logimind/` are intentionally not created until they contain
real implementation.

---

## 4. Installation and setup

### Requirements

- **Python 3.10 or newer** (CI uses Python 3.10)
- **Git**
- `jsonschema` for the validator, generator, and feasibility checker
- `pytest` and `ruff` for the optional development extras

```bash
git clone https://github.com/NTbankey1/LogiMind.git
cd LogiMind

python3 --version                  # confirm 3.10+
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e ".[dev]"            # or: pip install jsonschema pytest
```

The legacy prototype needs only the standard library. `.env.example` documents
proposed backend/solver settings; copy it to `.env` only when those components
exist. `.env` is ignored by Git.

---

## 5. Running and testing

All commands run from the repository root.

### Validate the canonical fixtures

```bash
python scripts/validate_dataset.py data/samples/
```

Expected: ten `[PASS]` lines, `10 datasets validated.`, `0 validation errors.`,
exit code `0`. Infeasible fixtures still pass structural validation; feasibility
is assessed separately.

### Generate a reproducible benchmark

```bash
python scripts/generate_dataset.py \
  --warehouses 4 --orders 20 --skus 5 --seed 20261111 \
  --output data/samples/generated.json
```

The same arguments and seed produce byte-identical JSON on the same Python
version. Generated datasets are feasible by construction.

### Check feasibility

```bash
python scripts/check_feasibility.py data/samples/sample_small.json
python scripts/check_feasibility.py data/samples/sample_infeasible.json
python scripts/check_feasibility.py data/samples/edge_infeasible_stock.json
python scripts/check_feasibility.py data/samples/sample_small.json --json
```

Statuses: `FEASIBLE`, `INFEASIBLE`, `UNKNOWN` (search limit), `INVALID`. Exit
codes: `0` for a completed proof, `1` for `INVALID`, `2` for `UNKNOWN`.

### Automated tests

```bash
python -m unittest discover -s tests -v
python -m pytest tests/ -v        # optional
```

The TV2 suite covers schema rules, semantic integrity, generator determinism,
every fixture's feasibility status, search-limit handling, input immutability, and
assignment invariants. See [tests/README.md](tests/README.md).

### Run the legacy prototype

```bash
python scripts/validate_orders.py
```

Reads `data/legacy/benchmark_data.json` by default and prints a Vietnamese
allocation log. It does not implement Policy A.

### Validate JSON syntax

```bash
python -m json.tool data/samples/sample_small.json > /dev/null
python -m json.tool data/legacy/benchmark_data.json > /dev/null
```

### CI checks

[.github/workflows/ci.yml](.github/workflows/ci.yml) runs repository hygiene
(JSON parsing, Markdown links, essential files, legacy-prototype smoke check) and
a TV2 job that installs `jsonschema`, validates all ten fixtures, runs the test
suite, asserts the expected feasibility status of every fixture, and verifies
generator determinism.

---

## 6. Team responsibilities

Roles follow [docs/team-responsibilities.md](docs/team-responsibilities.md).
Assignee names, GitHub handles, and deadlines remain **TBD**.

| Role | Scope | Current repository evidence |
| :--- | :--- | :--- |
| **TV1** | Business analysis and mathematical modeling | Policy A model and requirements are present |
| **TV2** | Data and test datasets | Canonical schema, fixtures, generator, validator, feasibility oracle, tests, CI job |
| **TV3** | Optimization algorithms | Not started; intended under `src/logimind/algorithms/` |
| **TV4** | Frontend | Not started; intended under `frontend/` |
| **TV5** | Backend and database | Not started; intended under `src/logimind/backend/` |
| **TV6** | Integration, testing, reporting | TV2 suite exists; broader integration/E2E tests and reporting not started |

---

## 7. Known limitations and open cross-module decisions

- The legacy prototype and `data/legacy/benchmark_data.json` use a flat schema
  with aggregate capacity and Euclidean costs. They are documented in Appendix A
  of the data dictionary and are not valid Policy A solver input.
- `docs/api-contract.md`, `docs/project-overview.md`, and
  `docs/testing-strategy.md` still mention split shipments, penalties, or
  handling costs. These conflicts are recorded as project blockers (B-01/B-03,
  EDGE-03) and are owned by TV1/TV5/TV6; they are not part of the canonical TV2
  contract.
- No solver, backend, database, or frontend exists.
- ADR-001, ADR-002, and ADR-003 remain `PROPOSED`.
- The exhaustive oracle verifies existence, not optimality, and can return
  `UNKNOWN` at its state limit.
- TV3/TV5/TV6 still need to adopt the canonical Policy A schema and fixtures.

---

## 8. Documentation map

| Document | Contents |
| :--- | :--- |
| [docs/index.md](docs/index.md) | Documentation centre and role-based reading paths |
| [docs/project-overview.md](docs/project-overview.md) | Problem context, objectives, scope |
| [docs/requirements.md](docs/requirements.md) | Business requirements and acceptance tests |
| [docs/mathematical-model.md](docs/mathematical-model.md) | Policy A formulation and worked examples |
| [docs/data-dictionary.md](docs/data-dictionary.md) | Canonical Policy A contract + legacy prototype Appendix A |
| [data/README.md](data/README.md) | Dataset catalogue and commands |
| [scripts/README.md](scripts/README.md) | Validator, generator, feasibility checker, legacy prototype |
| [src/README.md](src/README.md) | Intended Python package layout |
| [tests/README.md](tests/README.md) | Test suite and planned broader layout |
| [docs/architecture.md](docs/architecture.md) | Proposed components, paths, and data flow |
| [docs/api-contract.md](docs/api-contract.md) | Proposed REST endpoints and payloads |
| [docs/testing-strategy.md](docs/testing-strategy.md) | Test tiers, invariants, edge cases |
| [docs/integration-guide.md](docs/integration-guide.md) | Module handoff checklists |
| [docs/team-responsibilities.md](docs/team-responsibilities.md) | Role matrix (assignees TBD) |
| [docs/decisions/README.md](docs/decisions/README.md) | ADR index and status definitions |
| [docs/project-management/project-status.md](docs/project-management/project-status.md) | Evidence-based project status |
| [docs/project-management/repository-cleanup-plan.md](docs/project-management/repository-cleanup-plan.md) | Repository cleanup audit and record |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Branch, commit, PR, and review workflow |

---

## 9. Contributing

All changes go through a Pull Request targeting `main`; direct pushes are not
permitted. See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, Conventional
Commits, review requirements, and conflict handling.
