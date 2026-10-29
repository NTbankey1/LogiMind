# Integration & Module Handoff Guide: LogiMind

## 1. Overview & Handoff Principles

To enable 6 members (TV1 through TV6) to work concurrently without blocking each other or causing integration bottlenecks, development is governed by **explicit handoff contracts**.

Every module boundary has:
- A designated provider and consumer.
- Clearly specified input and output formats.
- A standardized **Handoff Checklist** that must be fulfilled before a feature branch is merged into `main`.

---

## 2. Cross-Role Dependency & Handoff Map

```mermaid
flowchart TD
    TV1["TV1: Mathematical Model & Rules"] -->|Formulation Contract| TV3["TV3: Baseline & MILP Algorithms"]
    TV1 -->|Business Rules| TV2["TV2: Data & Datasets"]
    
    TV2 -->|Sample Datasets & Schemas| TV3
    TV2 -->|Database Seed Fixtures| TV5["TV5: Backend & SQLite"]
    TV2 -->|Edge-case Fixtures| TV6["TV6: QA & Integration"]
    
    TV3 -->|Solver Callable / Adapter| TV5
    TV3 -->|Benchmark Results| TV6
    
    TV4["TV4: Frontend UI"] <-->|API Contract JSON| TV5
    
    TV5 -->|Integrated Endpoints| TV6
    TV4 -->|E2E Flow UI| TV6
    
    TV6 -->|Final Demo & Test Report| Faculty["Faculty & Stakeholders"]
```

---

## 3. Standard Module Handoff Checklists

Whenever a role completes a milestone, they must verify and publish their checklist in the corresponding Pull Request.

### 3.1 TV1 (Mathematical Model) $\to$ TV3 & TV2
- [ ] **Artifact:** `docs/mathematical-model.md` fully formalized.
- [ ] **Inputs & Parameters:** Clear index notation, unit specifications, and parameter boundaries.
- [ ] **Constraints:** Unambiguous mathematical equations for capacity, inventory, and split penalties.
- [ ] **Infeasibility Policy:** Concrete rule for handling over-demand (hard error vs. slack penalty).
- [ ] **Verification:** Manual verification on a 2-warehouse toy example documented.
- [ ] **Downstream Coordination:** Walkthrough meeting completed with TV3 and TV2.

---

### 3.2 TV2 (Data & Benchmark Datasets) $\to$ TV3, TV5, TV6
- [ ] **Artifacts:** `data/samples/` containing small, medium, and edge-case benchmark files (JSON/CSV).
- [ ] **Schema Conformance:** Data strictly satisfies `docs/data-dictionary.md`.
- [ ] **Validation Script:** Executable data validator script (`scripts/validate_datasets.py` or equivalent).
- [ ] **Known Limitations:** Documented edge cases (e.g. intentionally infeasible fixtures).
- [ ] **Downstream Coordination:** TV3 and TV5 verified datasets load cleanly in their environments.

---

### 3.3 TV3 (Algorithms) $\to$ TV5 & TV6
- [ ] **Artifacts:** Algorithm modules under `src/algorithms/` exposing a standard callable:
  `solve_allocation(problem_data: ProblemInput, algorithm: str) -> SolutionOutput`.
- [ ] **Baseline Implementation:** Greedy or nearest-warehouse heuristic fully operational.
- [ ] **MILP Implementation:** Solver model formulated, bounded, and tested.
- [ ] **Reproducibility:** Solvers yield deterministic outputs on identical seeds/inputs.
- [ ] **Benchmark Proof:** Execution log showing MILP cost $\le$ Baseline cost on sample dataset.
- [ ] **Unit Tests:** High-coverage tests under `tests/test_algorithms/` passing cleanly.

---

### 3.4 TV4 (Frontend) $\to$ TV5 & TV6
- [ ] **Artifacts:** UI dashboard under `src/frontend/` (or web client folder).
- [ ] **API Mocking:** Frontend can run against mock JSON server adhering to `docs/api-contract.md`.
- [ ] **Visual Elements:**
  - Order batch selection / upload.
  - Cost comparison chart (Baseline vs. MILP).
  - Warehouse capacity utilization gauges.
  - Split shipment details table.
- [ ] **Responsive Design:** Functional on standard laptop screen resolutions.
- [ ] **Downstream Coordination:** Endpoints verified against TV5 live backend.

---

### 3.5 TV5 (Backend & Database) $\to$ TV4 & TV6
- [ ] **Artifacts:** REST API application under `src/backend/` and SQLite database models.
- [ ] **Contract Compliance:** Endpoints strictly adhere to `docs/api-contract.md`.
- [ ] **Solver Integration:** Backend successfully calls TV3 solver engine with proper timeout guards.
- [ ] **Persistence:** Run history and allocation plans successfully stored and retrieved from SQLite.
- [ ] **Error Handling:** Returns structured HTTP 400/422/504 errors on invalid requests or solver timeouts.
- [ ] **Local Run Script:** Documented command to boot server locally (e.g., `uvicorn src.backend.main:app`).

---

### 3.6 TV6 (Integration, Testing & Reporting) $\to$ Team & Faculty
- [ ] **Artifacts:** Automated test suites (`tests/`), validation workflows, final presentation report.
- [ ] **End-to-End Suite:** Automated script executing: Seed Data $\to$ Backend API $\to$ Solver $\to$ Database verification.
- [ ] **Negative & Infeasibility Tests:** All edge cases in `docs/testing-strategy.md` covered.
- [ ] **CI Pass:** GitHub Actions CI green on `main`.
- [ ] **Demo Guide:** Step-by-step walkthrough script prepared for final demonstration before the faculty.
