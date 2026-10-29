# Team Responsibilities & Deliverables: LogiMind

> **Project:** LogiMind — Multi-Warehouse Order Allocation & Fulfillment Optimization  
> **Team Roster:** 6 Functional Member Roles  
> **Note:** Member identities, GitHub handles, and sprint deadlines are tracked as `TBD` until officially submitted and verified.

---

## 1. Role Allocation Matrix

| Role Code | Functional Role | Assignee Name | GitHub Handle | Target Sprint Deadline | Current Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TV1** | Business Analysis & Mathematical Modeling | *TBD* | *TBD* | *TBD* | Planning |
| **TV2** | Data & Test Dataset | *TBD* | *TBD* | *TBD* | Planning |
| **TV3** | Optimization Algorithms | *TBD* | *TBD* | *TBD* | Planning |
| **TV4** | Frontend | *TBD* | *TBD* | *TBD* | Planning |
| **TV5** | Backend & Database | *TBD* | *TBD* | *TBD* | Planning |
| **TV6** | Integration, Testing & Reporting | *TBD* | *TBD* | *TBD* | Planning |

---

## 2. Detailed Role Specifications

### TV1 — Business Analysis & Mathematical Modeling
- **Primary Scope:**
  - Formulate business context, requirements, and logistics constraints.
  - Define indices, decision variables, parameters, objective functions, and mathematical constraints.
  - Specify the unassigned order policy and handle edge/infeasible conditions.
- **Key Deliverables:**
  - `docs/mathematical-model.md` (Formal formulation).
  - Business rules section in `docs/requirements.md`.
  - Toy problem hand-calculation proof.
- **Dependencies:** None (Initiates modeling foundation).
- **Completion Criteria:**
  - Mathematical model validated by team and faculty advisor.
  - All constraints and variables approved by TV3 for computational solvability.

---

### TV2 — Data & Test Dataset
- **Primary Scope:**
  - Design data schemas for warehouses, SKUs, inventory levels, order lines, and shipping rate matrices.
  - Generate synthetic benchmark datasets (small, medium, large, and pathological edge cases).
  - Provide database seed files and data loading scripts.
- **Key Deliverables:**
  - `docs/data-dictionary.md`.
  - `data/samples/` (Benchmark datasets in JSON/CSV).
  - Dataset generator and schema validator scripts (`scripts/`).
- **Dependencies:** TV1 (Requires mathematical parameter definitions).
- **Completion Criteria:**
  - Datasets conform 100% to data dictionary schemas.
  - Contains at least 1 feasible benchmark and 1 guaranteed infeasible edge-case dataset.

---

### TV3 — Optimization Algorithms
- **Primary Scope:**
  - Implement Baseline Heuristic algorithm (e.g. Nearest Warehouse, Greedy Single-Warehouse).
  - Implement MILP Optimization model using Python solver libraries (PuLP / OR-Tools / SciPy).
  - Measure execution time, optimality gap, and warehouse utilization.
- **Key Deliverables:**
  - Algorithm module in `src/algorithms/`.
  - Solver abstraction interface / callable adapter.
  - Benchmark comparison report (Baseline vs. MILP).
  - Unit tests for optimization correctness.
- **Dependencies:** TV1 (Mathematical formulation) & TV2 (Benchmark datasets).
- **Completion Criteria:**
  - MILP achieves $\le$ cost compared to Baseline on standard benchmarks.
  - Invariants strictly maintained (zero inventory or capacity violations).

---

### TV4 — Frontend
- **Primary Scope:**
  - Design and build user interface for scenario configuration and visualization.
  - Implement order allocation summary dashboard (cost breakdown, split shipment rates).
  - Visualize warehouse capacity utilization and order routing.
- **Key Deliverables:**
  - Frontend web application in `src/frontend/` (or UI module).
  - Interactive allocation dashboard and charts.
  - Responsive layout and clear error status feedback.
- **Dependencies:** TV5 (API endpoints and mock responses).
- **Completion Criteria:**
  - Users can select a dataset, trigger a solve run, and visually inspect results without manual console commands.

---

### TV5 — Backend & Database
- **Primary Scope:**
  - Build REST API services to manage datasets, orchestrate solver runs, and serve results.
  - Implement relational database persistence using SQLite.
  - Implement input data validation, error handling, and solver timeout guards.
- **Key Deliverables:**
  - Backend API application in `src/backend/`.
  - Database schema models and migration scripts.
  - Standardized API endpoints adhering to `docs/api-contract.md`.
- **Dependencies:** TV3 (Algorithm adapter) & TV2 (Data schemas).
- **Completion Criteria:**
  - All proposed endpoints in `docs/api-contract.md` implemented, validated, and passing integration tests.

---

### TV6 — Integration, Testing & Reporting
- **Primary Scope:**
  - Establish automated test harness and CI quality gates.
  - Implement cross-module integration tests and regression suites.
  - Audit system against functional requirements.
  - Aggregate final benchmark reports and prepare demonstration slides/materials for faculty.
- **Key Deliverables:**
  - Test suites in `tests/` (unit, integration, and end-to-end).
  - `docs/testing-strategy.md` & `docs/integration-guide.md`.
  - Final project report and demonstration script.
- **Dependencies:** TV1 through TV5 (All deliverables).
- **Completion Criteria:**
  - 100% pass rate on automated CI test suites.
  - Successful rehearsal of live end-to-end demo before project presentation.
