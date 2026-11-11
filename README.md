# LogiMind

LogiMind is a decision-support project for the **Multi-Warehouse Order Allocation Problem (MWOAP)**: assigning customer orders to fulfillment warehouses while respecting stock and capacity limits, and comparing a simple heuristic against a Mixed-Integer Linear Programming (MILP) formulation.

The repository is currently at the **foundation and prototype stage**. Only the standalone allocation script is executable today, and it reads just one of the two JSON datasets; the API, database, frontend, MILP solver, and automated test suite are specified but not implemented. See [Current status](#2-current-status).

---

## 1. Problem statement

E-commerce fulfillment networks operate several warehouses. Assigning each order to the nearest warehouse can exhaust that warehouse's stock or throughput capacity and force later orders onto more expensive routes. LogiMind is intended to:

- read a batch of orders, warehouse capacities, per-SKU stock, and shipping costs;
- allocate each order to a warehouse, or record it as unassigned (depending on the chosen policy);
- compare a baseline heuristic with an optimal MILP allocation on the same input;
- report shipping cost, penalty cost, utilization, and runtime.

**Out of scope (documented):** multi-stop vehicle routing, demand forecasting, payments, HR, WMS/ERP integration, and real-time data feeds. See [docs/project-overview.md](docs/project-overview.md) and [docs/requirements.md](docs/requirements.md).

---

## 2. Current status

| Area | Status | Evidence |
| :--- | :--- | :--- |
| Standalone allocation prototype | **Implemented** | `validate_orders.py` (Python standard library only) |
| Primary benchmark data | **Implemented** | `benchmark_data.json` (3 warehouses, 2 orders) |
| Second sample fixture | **Present, not consumed** | `data/samples/sample_small.json` |
| Formal model and requirements | **Draft / proposed** | [docs/mathematical-model.md](docs/mathematical-model.md), [docs/requirements.md](docs/requirements.md) |
| Architecture, API contract, ADRs | **Proposed, not approved** | [docs/architecture.md](docs/architecture.md), [docs/api-contract.md](docs/api-contract.md), [docs/decisions/README.md](docs/decisions/README.md) |
| Backend API and SQLite persistence | **Not started** | `src/` contains only a placeholder README; ADR-002/ADR-003 are `PROPOSED` |
| Frontend | **Not started** | No frontend files; ADR-004 has not been written |
| MILP and packaged baseline algorithms | **Not started** | No `src/algorithms/` implementation; the root script is a prototype |
| Automated tests | **Not started** | `tests/` contains only a placeholder README; CI has no test job |
| CI repository-hygiene checks | **Implemented** | [.github/workflows/ci.yml](.github/workflows/ci.yml) |

### What the current prototype does

`validate_orders.py` loads `benchmark_data.json`, computes the Euclidean distance between each order's destination and each warehouse, and assigns the **whole order** to the nearest warehouse that has enough aggregate free capacity (`capacity - current_occupancy`). It prints the assignment log and updates occupancy only in memory.

It does **not** implement the documented MILP model: it has no per-SKU inventory check, no shipping-cost matrix $c_{ij}$, no unassigned-order penalty $P_i$, no split-shipment decision, and no optimality guarantees. It is a nearest-first baseline proof of concept, not the optimization engine described below.

---

## 3. Mathematical model and business constraints

The current formulation is documented in [docs/mathematical-model.md](docs/mathematical-model.md) (Vietnamese) with supporting requirements in [docs/requirements.md](docs/requirements.md). Both documents describe a **proposal**, not a team-approved final policy.

### Policy B (proposed primary policy)

**Sets and parameters**

| Symbol | Meaning |
| :--- | :--- |
| $I$, $J$, $K$ | Orders, warehouses, and SKUs |
| $q_{ik}$ | Quantity of SKU $k$ required by order $i$ |
| $s_{jk}$ | Available stock of SKU $k$ at warehouse $j$ |
| $C_j$ | Maximum **number of orders** warehouse $j$ can process in the batch |
| $c_{ij}$ | Cost of shipping the entire order $i$ from warehouse $j$ |
| $P_i$ | Penalty if order $i$ is left unassigned |
| $E \subseteq I \times J$ | Allowed order–warehouse pairs |

**Decision variables:** $x_{ij} \in \{0,1\}$ equals 1 when order $i$ is assigned to warehouse $j$; $u_i \in \{0,1\}$ equals 1 when order $i$ is unassigned.

**Objective**

$$
\min Z = \sum_{(i,j)\in E} c_{ij}x_{ij} + \sum_{i\in I} P_i u_i
$$

**Constraints**

$$
\sum_{j\in J} x_{ij} + u_i = 1 \quad \forall i \in I
\qquad\text{(exactly one state per order)}
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
x_{ij}, u_i \in \{0,1\}, \qquad x_{ij} = 0 \ \ \forall (i,j)\notin E
$$

**Policy A (alternative):** every order must be assigned ($\sum_j x_{ij}=1$), there is no $u_i$ or penalty, and the instance may be infeasible.

**Documented baseline:** process orders in ascending string order; choose the cheapest allowed warehouse that still has all required SKUs and free capacity; under policy B, leave the order unassigned when the cheapest shipping cost exceeds $P_i$. Ties break by warehouse ID.

The model's example uses 3 orders, 2 warehouses, and 2 SKUs and yields an optimal objective of 34 for policy B.

---

## 4. System architecture

### Implemented today

```text
benchmark_data.json  ->  validate_orders.py  ->  console output
(3 warehouses, 2 orders)   (nearest feasible warehouse, aggregate capacity)
```

There is no persistent storage, HTTP API, or user interface in the current codebase.

### Planned architecture (not implemented)

The planned three-tier design in [docs/architecture.md](docs/architecture.md) is:

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
Benchmark fixtures + automated tests (pytest)
```

The technology choices are recorded as **`PROPOSED`** ADRs: PuLP/CBC ([ADR-001](docs/decisions/0001-choice-of-optimization-solver-library.md)), FastAPI ([ADR-002](docs/decisions/0002-choice-of-backend-framework.md)), and SQLite ([ADR-003](docs/decisions/0003-choice-of-database-engine.md)). No ADR has `ACCEPTED` status.

---

## 5. Repository structure

```text
LogiMind/
├── .github/
│   ├── workflows/ci.yml            # Repository hygiene: JSON, Markdown links, essential files
│   ├── pull_request_template.md
│   └── ISSUE_TEMPLATE/
├── .editorconfig
├── .env.example                    # Template for proposed backend configuration
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CLAUDE.md                       # Contributor/agent technical guidelines
├── CONTRIBUTING.md                 # Git workflow and PR rules
├── README.md
├── benchmark_data.json             # Dataset read by validate_orders.py
├── data-dictionary.md              # Legacy flat schema for benchmark_data.json
├── validate_orders.py              # Current standalone allocation prototype
├── LogiMind_phantich.docx          # Project analysis document (binary)
├── data/
│   ├── README.md                   # Dataset tracking policy
│   └── samples/sample_small.json   # Alternative-schema toy fixture
├── docs/
│   ├── index.md
│   ├── project-overview.md
│   ├── requirements.md
│   ├── mathematical-model.md
│   ├── architecture.md
│   ├── api-contract.md
│   ├── data-dictionary.md          # Proposed relational schema
│   ├── testing-strategy.md
│   ├── integration-guide.md
│   ├── team-responsibilities.md
│   ├── git-workflow.md
│   └── decisions/                  # ADR index and ADR-001..003 (all PROPOSED)
├── scripts/README.md               # Placeholder; no scripts implemented
├── src/README.md                   # Placeholder; no source package implemented
└── tests/README.md                 # Placeholder; no automated tests implemented
```

Note: `data-dictionary.md` (repository root) and `docs/data-dictionary.md` describe **different schemas** and are not yet reconciled.

---

## 6. Installation and setup

### Requirements

- **Python 3.10 or newer** (CI uses Python 3.10)
- **Git**
- No third-party Python packages are required by the current script. The repository does not yet contain `requirements.txt` or `pyproject.toml`; solver and backend dependencies will be added when those components are implemented.

### Local setup

```bash
git clone https://github.com/NTbankey1/LogiMind.git
cd LogiMind

python3 --version          # confirm 3.10+
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

The current prototype does not read environment variables. [.env.example](.env.example) documents the proposed backend and solver settings; copy it to `.env` only when those components exist. `.env` is ignored by Git.

---

## 7. Execution and testing

### Run the allocation prototype

From the repository root:

```bash
python3 validate_orders.py
```

The script reads `benchmark_data.json` relative to the working directory and prints a Vietnamese allocation log. It does not write files or update the JSON input.

### Automated tests

There is currently **no automated test suite**. `tests/` contains only a placeholder README, and CI does not run `pytest`; running `pytest tests/ -v` would collect no tests.

### Checks that do run

CI ([.github/workflows/ci.yml](.github/workflows/ci.yml)) verifies:

- every JSON file under `data/samples/` parses;
- every internal Markdown link resolves;
- essential repository files exist.

Reproduce the JSON check locally:

```bash
python3 -m json.tool data/samples/sample_small.json > /dev/null
python3 -m json.tool benchmark_data.json > /dev/null
```

Full code-quality and integration testing will be added with the backend and solver.

---

## 8. Team responsibilities

Roles follow [docs/team-responsibilities.md](docs/team-responsibilities.md). Assignee names, GitHub handles, and deadlines are recorded there as **TBD**; no progress claims are made here beyond the artifacts visible in the repository.

| Role | Functional scope | Primary deliverables | Repository status |
| :--- | :--- | :--- | :--- |
| **TV1** | Business analysis and mathematical modeling | `docs/mathematical-model.md`, business rules in `docs/requirements.md` | Draft model and requirements present; policy not approved |
| **TV2** | Data and benchmark datasets | `docs/data-dictionary.md`, `data/samples/` | One sample fixture; two conflicting schemas |
| **TV3** | Optimization algorithms | Baseline and MILP modules under `src/algorithms/` | Not started; root prototype only |
| **TV4** | Frontend | UI under `src/frontend/` | Not started |
| **TV5** | Backend and database | FastAPI service, SQLite persistence | Not started |
| **TV6** | Integration, testing, and reporting | `tests/`, CI quality gates, benchmark report | Not started; CI is hygiene-only |

---

## 9. Known limitations and open business-rule decisions

The following conflicts are present in the current documentation and must be resolved by the team before implementing the solver or API. They are listed here so no reader assumes the rules are settled.

| Rule | Documented in | Conflicting source | Decision needed |
| :--- | :--- | :--- | :--- |
| **Warehouse capacity** | `C_j` counts **orders** per batch (`docs/mathematical-model.md` §1, §3.4; `docs/requirements.md` §2) | `capacity`/`current_occupancy` count **item units** in `benchmark_data.json`, root `data-dictionary.md`, and `validate_orders.py`; `docs/data-dictionary.md` says "units or orders" | Define one unit and update schema, data, and code |
| **SKU-level stock** | Required as $s_{jk}$ (model §3.3) | Absent from `benchmark_data.json`, root `data-dictionary.md`, and `validate_orders.py`; present in `docs/data-dictionary.md` and `data/samples/sample_small.json` | Confirm inventory source and remove aggregate-only checks |
| **Shipping cost $c_{ij}$** | Precomputed whole-order cost per order–warehouse pair | Euclidean distance in `validate_orders.py`; zone/weight rates in `docs/data-dictionary.md`; per-order `shipping_costs` in `sample_small.json` and the API contract | Choose one cost definition and make data and code match |
| **Unassigned penalty $P_i$** | Per-order value required in input (model §1, §3.6; requirements §3) | Missing from `benchmark_data.json`, root dictionary, and script; `sample_small.json` uses a global `unassigned_penalty` | Decide per-order vs global penalty and add it to the canonical schema |
| **Single vs split shipment** | One warehouse per order (binary $x_{ij}$; requirements §2) | Split shipments and split penalties appear in `docs/project-overview.md`, `docs/api-contract.md`, `docs/testing-strategy.md` (EDGE-03), `docs/architecture.md`, and `docs/integration-guide.md` | Approve or remove split-shipment support everywhere |
| **Handling cost** | Not part of the objective in the mathematical model | Included in `docs/project-overview.md` and the API contract response (`handling_cost`) | Confirm whether handling cost belongs in the objective |

Additional limitations:

- `data/samples/sample_small.json` claims to match the hand-calculated example in `docs/mathematical-model.md`, but it uses 2 orders and 1 SKU while the example uses 3 orders and 2 SKUs.
- Two data dictionaries (`data-dictionary.md` and `docs/data-dictionary.md`) describe incompatible schemas.
- No dependency manifest, packaging configuration, automated tests, API, database, or frontend exists yet.
- The CI workflow checks repository hygiene only; it does not execute application tests.
- Role-based identifiers (TV1–TV6) are used throughout the existing documents; contributor-facing workflow rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 10. Documentation map

| Document | Contents |
| :--- | :--- |
| [docs/project-overview.md](docs/project-overview.md) | Problem context, objectives, scope |
| [docs/requirements.md](docs/requirements.md) | Business requirements, validation rules, acceptance tests T1–T9 |
| [docs/mathematical-model.md](docs/mathematical-model.md) | MILP formulation, policies A/B, worked examples |
| [docs/architecture.md](docs/architecture.md) | Planned components, data flow, technology evaluation |
| [docs/api-contract.md](docs/api-contract.md) | Proposed REST endpoints and payloads |
| [docs/data-dictionary.md](docs/data-dictionary.md) | Proposed relational schema |
| [data-dictionary.md](data-dictionary.md) | Legacy schema for `benchmark_data.json` |
| [docs/testing-strategy.md](docs/testing-strategy.md) | Test tiers, invariants, edge cases |
| [docs/integration-guide.md](docs/integration-guide.md) | Module handoff checklists |
| [docs/team-responsibilities.md](docs/team-responsibilities.md) | Role matrix (assignees TBD) |
| [docs/decisions/README.md](docs/decisions/README.md) | ADR index and status definitions |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Branch, commit, PR, and review workflow |

---

## 11. Contributing

All changes go through a Pull Request targeting `main`; direct pushes are not permitted. See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, Conventional Commits, review requirements, and conflict handling.
