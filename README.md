# LogiMind

LogiMind is a decision-support project for the **Multi-Warehouse Order Allocation
Problem (MWOAP)**: assigning each customer order to exactly one fulfillment
warehouse while respecting per-SKU stock and order-count capacity, then comparing
a simple heuristic against a Mixed-Integer Linear Programming (MILP) allocation.

The repository is at the **foundation + data-contract stage**. The TV2 dataset
workstream is implemented: canonical Policy A schema, benchmark fixtures, a
deterministic generator, a validator, an exhaustive small-instance feasibility
oracle, automated tests, and a CI job. The solver, backend, database, and frontend
are specified but not implemented. A legacy standalone prototype remains for
reference.

---

## 1. Problem statement

E-commerce fulfillment networks operate several warehouses. Assigning each order
to the nearest warehouse can exhaust that warehouse's stock or throughput capacity
and force later orders onto more expensive routes. LogiMind is intended to:

- read a batch of orders, warehouse capacities, per-SKU stock, and shipping costs;
- allocate **every** order to exactly one warehouse (Policy A);
- compare a baseline heuristic with an optimal MILP allocation on the same input;
- report shipping cost, utilization, and runtime.

**Out of scope (documented):** multi-stop vehicle routing, demand forecasting,
payments, HR, WMS/ERP integration, and real-time data feeds. See
[docs/project-overview.md](docs/project-overview.md) and
[docs/requirements.md](docs/requirements.md).

---

## 2. Current status

| Area | Status | Evidence |
| :--- | :--- | :--- |
| Canonical data contract | **Implemented (Policy A)** | [docs/data-dictionary.md](docs/data-dictionary.md), [data/schema/dataset.schema.json](data/schema/dataset.schema.json) |
| Benchmark and edge-case fixtures | **Implemented** | Ten files under [data/samples/](data/samples/); catalogue in [data/README.md](data/README.md) |
| Dataset generator | **Implemented** | [scripts/generate_dataset.py](scripts/generate_dataset.py) (deterministic, feasible by construction) |
| Dataset validator | **Implemented** | [scripts/validate_dataset.py](scripts/validate_dataset.py) (schema + semantic checks) |
| Feasibility oracle | **Implemented (small instances)** | [scripts/check_feasibility.py](scripts/check_feasibility.py) |
| Automated TV2 tests | **Implemented** | [tests/test_datasets.py](tests/test_datasets.py) (60 tests) |
| CI | **Configured** | [.github/workflows/ci.yml](.github/workflows/ci.yml): repository hygiene + TV2 dataset job |
| Allocation policy | **Decided: Policy A** | [ADR-004](docs/decisions/0004-allocation-policy-a.md) |
| Legacy allocation prototype | **Implemented (not Policy A)** | `validate_orders.py`, `benchmark_data.json` |
| Formal model and requirements | **Present; policy A selected** | [docs/mathematical-model.md](docs/mathematical-model.md), [docs/requirements.md](docs/requirements.md) |
| Architecture, API contract, ADR-001–003 | **Proposed, not approved** | [docs/architecture.md](docs/architecture.md), [docs/api-contract.md](docs/api-contract.md) |
| Backend API and SQLite persistence | **Not started** | `src/` contains only a placeholder README |
| Frontend | **Not started** | No frontend files |
| MILP and packaged baseline algorithms | **Not started** | No `src/algorithms/` implementation |

### Legacy prototype

`validate_orders.py` loads `benchmark_data.json`, computes Euclidean distances, and
assigns each whole order to the nearest warehouse with enough aggregate free
capacity. It uses a legacy flat schema with aggregate capacity, no per-SKU
inventory, and no shipping-cost matrix. It is **not** the Policy A model and is
retained only for historical comparison. Do not use `benchmark_data.json` as
solver input.

---

## 3. Allocation policy and data contract

The Project Lead selected **Policy A**; the decision is recorded in
[ADR-004](docs/decisions/0004-allocation-policy-a.md). The authoritative field
definitions, units, and validation rules live in
[docs/data-dictionary.md](docs/data-dictionary.md).

### Policy A

**Sets and parameters**

| Symbol | Meaning |
| :--- | :--- |
| $I$, $J$, $K$ | Orders, warehouses, and SKUs |
| $q_{ik}$ | Quantity of SKU $k$ required by order $i$ |
| $s_{jk}$ | Available stock of SKU $k$ at warehouse $j$ |
| $C_j$ | Maximum **number of orders** warehouse $j$ can process |
| $c_{ij}$ | Cost of shipping the entire order $i$ from warehouse $j$ |
| $E \subseteq I \times J$ | Allowed order–warehouse pairs (route exists in `shipping_costs`) |

**Decision variable:** $x_{ij} \in \{0,1\}$ equals 1 when order $i$ is assigned to
warehouse $j$.

**Objective**

$$
\min Z = \sum_{(i,j)\in E} c_{ij}x_{ij}
$$

**Constraints**

$$
\sum_{j\in J} x_{ij} = 1 \quad \forall i \in I
\qquad\text{(exactly one warehouse, no unassigned orders)}
$$

$$
\sum_{i\in I} q_{ik}x_{ij} \le s_{jk} \quad \forall j \in J,\ \forall k \in K
\qquad\text{(per-SKU stock)}
$$

$$
\sum_{i\in I} x_{ij} \le C_j \quad \forall j \in J
\qquad\text{(order-count capacity)}
$$

$$
x_{ij} \in \{0,1\}, \qquad x_{ij} = 0 \ \ \forall (i,j)\notin E
$$

There is no split shipment, no unassigned variable, no unassigned penalty, and no
handling cost. If no complete allocation exists, the instance is
**mathematically infeasible** — it is still structurally valid.

Policy B (penalty-based, split/unassigned orders) is retained only as historical
material in `docs/mathematical-model.md` §3 and `docs/requirements.md`.

### Dataset example

```json
{
  "schema_version": "1.0",
  "dataset_id": "sample-small",
  "name": "Small Feasible Benchmark",
  "description": "Small 2-warehouse, 3-order, 2-SKU Policy A benchmark.",
  "policy": "A",
  "skus": [{ "sku_id": "SKU-A", "name": "Product Alpha" }],
  "warehouses": [{
    "warehouse_id": "WH-01",
    "name": "Warehouse North",
    "capacity_orders": 2,
    "inventory": { "SKU-A": 10 }
  }],
  "orders": [{
    "order_id": "ORD-001",
    "items": { "SKU-A": 2 },
    "shipping_costs": { "WH-01": 4.0 }
  }]
}
```

---

## 4. System architecture

### Implemented today (TV2 data layer + legacy prototype)

```text
data/schema/dataset.schema.json
        |
        v
data/samples/*.json  ->  scripts/validate_dataset.py  ->  PASS / FAIL
        |                        |
        |                        +-> scripts/check_feasibility.py -> FEASIBLE / INFEASIBLE / UNKNOWN
        v
scripts/generate_dataset.py  ->  new deterministic, feasible dataset

benchmark_data.json  ->  validate_orders.py  ->  console output   (legacy, non-Policy-A)
```

### Planned architecture (not implemented)

```text
React / Vite frontend
        |  HTTP (proposed /api/v1 contract)
        v
FastAPI backend  <-->  SQLite database
        |
        v
Optimization engine: baseline heuristic + MILP (PuLP/CBC proposed)
        ^
        |
Policy A datasets + automated tests
```

The solver, backend, and database technology choices remain `PROPOSED`:
PuLP/CBC ([ADR-001](docs/decisions/0001-choice-of-optimization-solver-library.md)),
FastAPI ([ADR-002](docs/decisions/0002-choice-of-backend-framework.md)), and SQLite
([ADR-003](docs/decisions/0003-choice-of-database-engine.md)). Only ADR-004
(Policy A) is `ACCEPTED`.

---

## 5. Repository structure

```text
LogiMind/
├── .github/workflows/ci.yml        # Hygiene job + TV2 dataset/test job
├── .editorconfig
├── .env.example                    # Template for proposed backend configuration
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CLAUDE.md                       # Contributor/agent technical guidelines
├── CONTRIBUTING.md
├── README.md
├── pyproject.toml                  # Packaging and dev/test extras
├── benchmark_data.json             # Legacy prototype input (not Policy A)
├── data-dictionary.md              # Deprecated pointer to docs/data-dictionary.md
├── validate_orders.py              # Legacy standalone allocation prototype
├── LogiMind_phantich.docx          # Project analysis document (binary)
├── data/
│   ├── README.md                   # Fixture catalogue and commands
│   ├── schema/dataset.schema.json  # Canonical JSON Schema (Draft 2020-12)
│   └── samples/*.json              # 10 Policy A fixtures
├── docs/
│   ├── index.md
│   ├── project-overview.md
│   ├── requirements.md
│   ├── mathematical-model.md
│   ├── architecture.md
│   ├── api-contract.md
│   ├── data-dictionary.md          # Canonical Policy A data dictionary
│   ├── testing-strategy.md
│   ├── integration-guide.md
│   ├── team-responsibilities.md
│   ├── git-workflow.md
│   └── decisions/                  # ADR index; ADR-001..003 PROPOSED, ADR-004 ACCEPTED
├── scripts/
│   ├── README.md
│   ├── validate_dataset.py
│   ├── generate_dataset.py
│   └── check_feasibility.py
├── src/README.md                   # Placeholder; no source package implemented
└── tests/
    ├── README.md
    └── test_datasets.py            # TV2 dataset/generator/feasibility tests
```

---

## 6. Installation and setup

### Requirements

- **Python 3.10 or newer** (CI uses Python 3.10)
- **Git**
- `jsonschema` for dataset validation, generation, and feasibility checking
- `pytest` and `ruff` for the optional development extras

```bash
git clone https://github.com/NTbankey1/LogiMind.git
cd LogiMind

python3 --version                  # confirm 3.10+
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e ".[dev]"            # or: pip install jsonschema pytest
```

The legacy prototype uses only the standard library. [.env.example](.env.example)
documents proposed backend/solver settings; copy it to `.env` only when those
components exist. `.env` is ignored by Git.

---

## 7. Execution and testing

All commands run from the repository root.

### Validate the committed fixtures

```bash
python scripts/validate_dataset.py data/samples/
```

Expected: ten `[PASS]` lines, `10 datasets validated.`, `0 validation errors.`,
exit code `0`. An infeasible fixture still passes; feasibility is a separate
question.

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
codes: `0` for a completed proof (`FEASIBLE`/`INFEASIBLE`), `1` for `INVALID`,
`2` for `UNKNOWN`.

### Automated tests

```bash
python -m unittest discover -s tests -v
# optional: python -m pytest tests/ -v
```

The TV2 suite covers schema rules, semantic integrity, generator determinism,
feasibility statuses for every fixture, search-limit handling, input immutability,
and assignment invariants. See [tests/README.md](tests/README.md).

### Run the legacy prototype

```bash
python3 validate_orders.py
```

Reads `benchmark_data.json` from the working directory and prints a Vietnamese
allocation log. It does not implement Policy A.

### CI checks

[.github/workflows/ci.yml](.github/workflows/ci.yml) preserves the existing
repository-hygiene checks (JSON parsing, internal Markdown links, essential files)
and adds a `tv2-datasets` job that installs `jsonschema`, validates every fixture,
runs the unittest suite, and asserts the expected feasibility status of
`sample_small`, `sample_infeasible`, and `edge_infeasible_stock`.

---

## 8. Team responsibilities

Roles follow [docs/team-responsibilities.md](docs/team-responsibilities.md).
Assignee names, GitHub handles, and deadlines are recorded there as **TBD**.

| Role | Functional scope | Repository status |
| :--- | :--- | :--- |
| **TV1** | Business analysis and mathematical modeling | Model and requirements present; Policy A selected; handoff refinements open |
| **TV2** | Data and benchmark datasets | **Implemented**: Policy A schema, 10 fixtures, generator, validator, feasibility oracle, tests, CI job |
| **TV3** | Optimization algorithms | Not started; baseline and MILP still to implement |
| **TV4** | Frontend | Not started |
| **TV5** | Backend and database | Not started |
| **TV6** | Integration, testing, and reporting | Not started; TV2 tests are the first automated suite |

---

## 9. Known limitations and open cross-module decisions

TV2's contract is settled on Policy A. Other documents still contain
pre-decision language and must be reconciled by their owners.

| Item | Current state | Owner / next step |
| :--- | :--- | :--- |
| Split shipments, unassigned penalties, handling cost | Still described in `docs/project-overview.md`, `docs/api-contract.md`, `docs/testing-strategy.md`, `docs/architecture.md`, and `docs/integration-guide.md` | TV4/TV5/TV6: align to Policy A; TV2's schema rejects these fields |
| Legacy prototype schema | `benchmark_data.json` and `validate_orders.py` use aggregate capacity and Euclidean costs | Retained for history; migrate only via an explicit decision |
| Large-instance optimization | No solver exists; the feasibility oracle is exponential | TV3: implement baseline + MILP against the Policy A contract |
| CI evidence | The TV2 job is configured in the workflow | Confirm the run on the Pull Request |
| Backend, database, frontend | Not implemented | TV5, TV4 |

Additional limitations:

- The exhaustive oracle verifies existence, not optimality, and can return
  `UNKNOWN` at its state limit.
- Role-based identifiers (TV1–TV6) are used throughout; contributor workflow rules
  are in [CONTRIBUTING.md](CONTRIBUTING.md).
- The binary `LogiMind_phantich.docx` remains the historical analysis source.

---

## 10. Documentation map

| Document | Contents |
| :--- | :--- |
| [docs/project-overview.md](docs/project-overview.md) | Problem context, objectives, scope |
| [docs/requirements.md](docs/requirements.md) | Business requirements, validation rules, acceptance tests T1–T9 |
| [docs/mathematical-model.md](docs/mathematical-model.md) | MILP formulations; Policy A is canonical |
| [docs/data-dictionary.md](docs/data-dictionary.md) | **Canonical Policy A data dictionary** |
| [data/schema/dataset.schema.json](data/schema/dataset.schema.json) | Machine-readable JSON Schema |
| [data/README.md](data/README.md) | Fixture catalogue and dataset commands |
| [scripts/README.md](scripts/README.md) | Generator, validator, and feasibility CLI reference |
| [tests/README.md](tests/README.md) | How to run and interpret the TV2 suite |
| [docs/architecture.md](docs/architecture.md) | Planned components and data flow |
| [docs/api-contract.md](docs/api-contract.md) | Proposed REST endpoints and payloads |
| [docs/testing-strategy.md](docs/testing-strategy.md) | Test tiers, invariants, edge cases |
| [docs/integration-guide.md](docs/integration-guide.md) | Module handoff checklists |
| [docs/team-responsibilities.md](docs/team-responsibilities.md) | Role matrix (assignees TBD) |
| [docs/decisions/README.md](docs/decisions/README.md) | ADR index and status definitions |
| [data-dictionary.md](data-dictionary.md) | Deprecated pointer to the canonical dictionary |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Branch, commit, PR, and review workflow |

---

## 11. Contributing

All changes go through a Pull Request targeting `main`; direct pushes are not
permitted. See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, Conventional
Commits, review requirements, and conflict handling.
