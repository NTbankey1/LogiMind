# LogiMind Task Tracker

> **Owner:** Project Lead / TV6
> **Last verified:** 2026-11-09
> **Status source:** Repository artifacts, commits, PRs, and CI runs on `origin/main` at `7424ba4`.
> **Assignment rule:** This tracker records the responsibilities already documented in [Team Responsibilities](../team-responsibilities.md). It does **not** change assignments. Names, GitHub handles, and deadlines remain `TBD` until the team confirms them.

---

## 1. Existing team responsibilities

The following scope is taken from [docs/team-responsibilities.md](../team-responsibilities.md). The source document lists every role as `Planning` and every assignee as `TBD`.

| Role | Responsibility | Documented primary deliverables | Documented dependencies | Identity |
| :--- | :--- | :--- | :--- | :--- |
| **TV1** | Business analysis and mathematical modeling | `docs/mathematical-model.md`; business rules in `docs/requirements.md`; toy-problem hand calculation; unassigned-order policy | None (initiates modeling) | Name / handle / deadline: `TBD` |
| **TV2** | Data and test datasets | `docs/data-dictionary.md`; `data/samples/` fixtures; dataset generator and schema validator under `scripts/` | TV1 parameter definitions | Name / handle / deadline: `TBD` |
| **TV3** | Optimization algorithms | Baseline and MILP implementation under `src/algorithms/`; solver adapter; benchmark comparison; unit tests | TV1 model; TV2 datasets | Name / handle / deadline: `TBD` |
| **TV4** | Frontend | UI application under `src/frontend/`; allocation dashboard; capacity/cost views; error feedback | TV5 API and mock responses | Name / handle / deadline: `TBD` |
| **TV5** | Backend and database | FastAPI application under `src/backend/`; SQLite models/migrations; API endpoints; validation and timeout handling | TV3 adapter; TV2 schemas | Name / handle / deadline: `TBD` |
| **TV6** | Integration, testing, reporting | `tests/` suites; CI quality gates; integration tests; benchmark report; final report and demo | TV1–TV5 deliverables | Name / handle / deadline: `TBD` |

> GitHub currently has **0 Issues and 0 milestones**; this tracker is the repository-based substitute until the Project Lead creates official issues. It is not an assignment mechanism.

---

## 2. Workstream tracker

Status vocabulary: **Completed**, **In Progress**, **Blocked**, **Not Started**, **Unable to Verify**.
“Evidence” means a repository artifact or GitHub record, not an estimate of effort.

### TV1 — Business requirements and mathematical model

| ID | Deliverable | Acceptance criteria | Status | Dependencies | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV1-01 | Approved policy decision (A or B) and parameter semantics | Decision recorded in an approved ADR or requirements revision; `C_j`, `c_ij`, `P_i`, split policy, and handling-cost scope are unambiguous | **Blocked** | Team approval; TV2 data implications | [model §3–§4](../mathematical-model.md); [requirements §3](../requirements.md) |
| TV1-02 | Requirements baseline for FR01–FR08 and T1–T9 | Requirements are reviewed, unambiguous, and traceable to test IDs | **In Progress** | TV1-01 | [requirements §5–§7](../requirements.md) |
| TV1-03 | Model handoff to TV2/TV3 with example verification | Worked example reproduced; handoff checklist evidence attached; model assumptions signed off | **Blocked** | TV1-01; TV2 schema | [model §6–§9](../mathematical-model.md); [integration-guide §3.1](../integration-guide.md) |

### TV2 — Data and test datasets

| ID | Deliverable | Acceptance criteria | Status | Dependencies | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV2-01 | Canonical data schema | One schema covers warehouses, inventory, orders/lines, costs, and penalties; field names/types/units are consistent with the approved model | **Blocked** | TV1-01 | [data-dictionary](../data-dictionary.md); [legacy dictionary](../../data-dictionary.md); conflicts noted in [PROJECT_STATUS](PROJECT_STATUS.md#4-blockers-and-dependencies) |
| TV2-02 | Benchmark fixtures | At least one feasible and one guaranteed-infeasible fixture, plus edge cases required by [testing-strategy](../testing-strategy.md); all pass schema validation | **In Progress** (partial) | TV2-01 | `benchmark_data.json`; [sample_small.json](../../data/samples/sample_small.json) |
| TV2-03 | Dataset generator and validator | Executable scripts validate schema and invariants; invalid fixtures are rejected with clear errors | **Not Started** | TV2-01 | `scripts/` contains only a README |
| TV2-04 | Data documentation reconciliation | One authoritative dictionary; README/sample descriptions match actual fixtures | **In Progress** | TV2-01 | [data/README.md](../../data/README.md) contains conflicting counts/ignore claims |

### TV3 — Optimization algorithms

| ID | Deliverable | Acceptance criteria | Status | Dependencies | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV3-01 | Baseline heuristic implementation | Implements the documented order/tie-break rule; consumes canonical input; returns assignments and metrics | **Not Started** | TV1-01, TV2-01 | [model §5](../mathematical-model.md); `src/` has only README |
| TV3-02 | MILP implementation | Implements the approved policy; respects stock and capacity constraints; reports status and objective components | **Not Started** | TV1-01, TV2-01, TV3-01 | [model §3](../mathematical-model.md) |
| TV3-03 | Solver adapter | Stable callable contract as specified by the integration guide; deterministic inputs/outputs; error and timeout behavior | **Not Started** | TV3-01, TV3-02 | [integration-guide §3.3](../integration-guide.md) |
| TV3-04 | Algorithm tests and benchmark report | Unit tests cover invariants and edge cases; MILP cost is not worse than baseline on standard fixtures; runtime/status recorded | **Not Started** | TV3-01–TV3-03; TV6 test harness | [testing-strategy](../testing-strategy.md); `tests/` has only README |

### TV4 — Frontend

| ID | Deliverable | Acceptance criteria | Status | Dependencies | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV4-01 | Frontend application scaffold | Application starts with documented command; no backend coupling required for mock mode | **Not Started** | TV5 API contract | No frontend files or manifest; [integration-guide §3.4](../integration-guide.md) |
| TV4-02 | Allocation dashboard | User can select/upload a dataset, trigger a run, and inspect assignments, costs, utilization, and errors | **Not Started** | TV4-01, TV5 API | [requirements FR01–FR07](../requirements.md) |
| TV4-03 | API integration | UI consumes the approved API contract and handles validation, infeasibility, and timeout responses | **Not Started** | TV4-02, TV5 implementation, TV1/TV5 sign-off | [api-contract](../api-contract.md) is `Proposed` |
| TV4-04 | E2E readiness evidence | Documented UI flow can be executed against the live backend for TV6 E2E testing | **Not Started** | TV4-03, TV5 implementation | [integration-guide §3.4](../integration-guide.md) |

*Split-shipment UI is conditional: the requirement conflicts with the mathematical model and must be resolved before TV4-02 acceptance.*

### TV5 — Backend and database

| ID | Deliverable | Acceptance criteria | Status | Dependencies | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV5-01 | API implementation | Endpoints match the approved API contract, including envelope, validation, and error semantics | **Not Started** | TV1-01, TV2-01, TV3-03 | [api-contract](../api-contract.md) is `Proposed` |
| TV5-02 | SQLite persistence | Schema/models and migrations persist runs, allocations, configuration, and metrics; database files are never committed | **Not Started** | TV2-01, TV5-01 | ADR-003 is `PROPOSED`; `.gitignore` on `main` does not ignore DB files |
| TV5-03 | Solver integration and timeout guard | Backend calls the solver adapter with a configurable timeout and returns documented statuses/errors | **Not Started** | TV3-03, TV5-01 | [integration-guide §3.5](../integration-guide.md) |
| TV5-04 | Backend tests | Contract and integration tests pass against SQLite and fixtures | **Not Started** | TV5-01–TV5-03; TV6 harness | `tests/` has only README |

### TV6 — Integration, testing, reporting

| ID | Deliverable | Acceptance criteria | Status | Dependencies | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV6-01 | Project-management documentation set | Status, tracker, integration plan, and test plan exist and are consistent with repository evidence | **In Progress** | None | This file; [PROJECT_STATUS](PROJECT_STATUS.md); [INTEGRATION_PLAN](INTEGRATION_PLAN.md); [TEST_PLAN](TEST_PLAN.md) |
| TV6-02 | Requirements traceability and test plan | T1–T9 and EDGE-01–05 mapped to test IDs, levels, prerequisites, and evidence | **In Progress** | TV1 requirements baseline | [TEST_PLAN](TEST_PLAN.md) |
| TV6-03 | Test harness | `pytest` structure, fixtures, and helpers exist; tests can run locally and in CI | **Not Started** | TV1-01, TV2-01 | `tests/` has only README |
| TV6-04 | CI test job | CI installs dependencies and runs the test suite; failures block merge | **Not Started** | TV6-03; Project Lead ruleset update | [ci.yml](../../.github/workflows/ci.yml) runs hygiene only |
| TV6-05 | Contract, integration, and E2E tests | Tests cover solver adapter, API, SQLite persistence, and the full dataset → API → solver → DB → UI flow | **Not Started** | TV3-03, TV5-01–TV5-03, TV4-04 | [testing-strategy](../testing-strategy.md) |
| TV6-06 | Bug tracking and verification workflow | Bugs have reproduction steps, severity, expected/actual, and closure evidence; issue templates are used | **Not Started** | Project Lead to enable issue workflow | `.github/ISSUE_TEMPLATE/` exists; 0 issues created |
| TV6-07 | Benchmark and final report | Baseline/MILP comparison, test summary, known limitations, demo script, and final report are produced from executed evidence | **Not Started** | TV1–TV5 deliverables; TV6-05 | [team-responsibilities](../team-responsibilities.md) |

---

## 3. Dependency summary

```text
TV1-01 (approved rules)
  -> TV2-01 (canonical schema)
      -> TV2-02/03 (fixtures + validator)
      -> TV3-01/02/03 (baseline, MILP, adapter)
          -> TV5-01/02/03 (API, SQLite, solver integration)
              -> TV4-01/02/03 (UI, dashboard, live API)
                  -> TV6-05 (contract/integration/E2E)
                      -> TV6-07 (benchmark + final report)
TV6-02/03/04 (traceability, harness, CI job) can start before TV3–TV5 complete.
```

---

## 4. Status evidence rules

- A task becomes **Completed** only when its acceptance criteria are demonstrated by a committed artifact, executed test output, or merged PR.
- A task is **Blocked** when its dependency is explicitly unresolved; the blocker is recorded in [PROJECT_STATUS §4](PROJECT_STATUS.md#4-blockers-and-dependencies).
- A task is **In Progress** only when an artifact exists in the repository, not when work is merely planned or discussed.
- Update the verification date and evidence link whenever a status changes.
- This tracker does not replace GitHub Issues. Once the Project Lead creates official issues/milestones, link them here rather than duplicating their state.

---

## 5. Known missing information requiring team confirmation

1. Which GitHub account owns each TV role.
2. Approval of policy A or B and the six business-rule conflicts listed in PROJECT_STATUS §4.
3. Canonical data schema, including capacity units and required penalty fields.
4. Whether split shipments and handling costs belong in the objective and API.
5. Target sprint dates and milestone definitions.
6. Ownership of the root-level prototype and datasets.
