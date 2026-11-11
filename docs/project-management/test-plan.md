# LogiMind Test Plan

> **Owner:** TV6 (Integration, Testing & Reporting)
> **Last verified:** 2026-11-09
> **Baseline:** `origin/main` at `7424ba4`
> **Principle:** No test is reported as passing unless it was executed and its output was observed. Planned tests are marked as planned, not completed.

---

## 1. Objectives and scope

This plan defines how TV6 will verify that LogiMind satisfies the requirements in [requirements.md](../requirements.md) and the invariants/edge cases in [testing-strategy.md](../testing-strategy.md). It covers unit, contract, integration, system, and end-to-end testing. It does **not** redefine business rules, API schemas, or algorithms owned by TV1–TV5.

**In scope:** allocation behavior, mathematical invariants, data validation, API contracts, persistence, solver integration, UI flow, and reporting evidence.
**Out of scope:** performance tuning beyond recorded benchmark metrics, deployment, and business-rule decisions that remain unapproved.

---

## 2. Current test inventory

| Item | State | Evidence |
| :--- | :--- | :--- |
| Automated test suite | **Not implemented** | `tests/` contains only a README |
| Test framework configuration | **Not present** | No `pytest.ini`, `pyproject.toml`, `conftest.py`, or dependency manifest |
| CI test execution | **Not present** | [.github/workflows/ci.yml](../../.github/workflows/ci.yml) runs JSON/Markdown/file checks only |
| JSON syntax validation | **Exists in CI** | `data/samples/*.json` parsed with `python -m json.tool` |
| Markdown link validation | **Exists in CI** | Internal relative links checked |
| Essential-file check | **Exists in CI** | README, CLAUDE, CONTRIBUTING, CHANGELOG, `.gitignore`, `.editorconfig`, `.gitattributes` |
| Prototype smoke run | **Manual only** | `python3 scripts/validate_orders.py` executed; printed assignments; no assertions |
| Requirement-based tests (T1–T9) | **Not implemented** | Requirements table exists, no test IDs execute |
| Edge-case tests (EDGE-01–05) | **Not implemented** | Testing-strategy table exists, no test files |
| API/DB/frontend/solver tests | **Not possible yet** | Modules do not exist |

**Conclusion:** CI is green, but it proves repository hygiene only. It does not prove allocation correctness, constraint satisfaction, or integration behavior.

---

## 3. Test levels and responsibilities

| Level | Purpose | Executed by | Prerequisites | Primary evidence |
| :--- | :--- | :--- | :--- | :--- |
| **Unit** | Verify functions, validators, heuristics, and cost calculations in isolation | Module owners (TV3/TV5); TV6 reviews evidence | Module code; canonical fixtures | Test command, pass/fail output, coverage report if available |
| **Contract** | Verify solver adapter and API boundaries against frozen contracts | TV6 with TV3/TV5 | G1 contracts; adapter/API implementation | Contract test output; request/response transcripts |
| **Integration** | Verify API ↔ solver ↔ SQLite behavior on canonical fixtures | TV6 with TV5 | G2 fixtures; G3 solver; G4 backend | Integration run log; DB read-back evidence |
| **System** | Verify end-to-end backend behavior, including invalid/infeasible/timeout cases | TV6 | G4 backend; G2 fixtures | System test report; status/HTTP evidence |
| **E2E** | Verify user flow from dataset selection to results display | TV6 with TV4 | G5 frontend; live backend | Recorded walkthrough; E2E test output |
| **Benchmark/performance** | Record Baseline vs MILP cost, runtime, status, and utilization | TV3 supplies; TV6 verifies | G3 solver; G2 fixtures | Benchmark table with environment and run configuration |

The testing tiers in [testing-strategy.md §2](../testing-strategy.md) remain the reference. Tooling mentioned there (`pytest`, optional Playwright/request tests) is **proposed**; nothing is installed or configured yet.

---

## 4. Requirements traceability — T1 to T9

Source: [requirements.md §7](../requirements.md) (T1–T9). “Preparable now” means test design/fixtures can be drafted without module code; execution still requires the prerequisites.

| Test ID | Requirement | Source | Level | Module under test | Preparable now? | Prerequisite | Expected evidence | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T1** | Small hand-calculated example matches cost and valid allocation, or exhaustive verification | requirements T1 | Unit + System | TV3 solver / independent checker | Test case design only | Approved model; solver; canonical fixture | Reproduced objective and assignment vs. hand calculation | **Blocked** |
| **T2** | Sufficient stock and capacity; all orders can be assigned | requirements T2 | Unit + Integration | Solver (Policy A) | Test case design only | Solver; canonical fixtures | Every order assigned to one warehouse; objective matches shipping cost | **Blocked** |
| **T3** | Cheapest warehouse missing one SKU is not assigned the whole order | requirements T3 | Unit | Baseline/MILP | Test case design only | Solver; per-SKU inventory | Assignment avoids invalid warehouse; invariant check | **Blocked** |
| **T4** | Cheapest warehouse at capacity is not exceeded; use another warehouse | requirements T4 | Unit + Integration | Solver capacity constraint | Test case design only | Capacity semantics; solver | Capacity usage ≤ `capacity_orders`; order assigned to an alternate eligible warehouse | **Blocked** |
| **T5** | Tight stock and capacity simultaneously respected | requirements T5 | Unit + Invariant | Solver | Test case design only | Solver; validator | All inventory/capacity invariants hold | **Blocked** |
| **T6** | Inability to fulfill all orders is reported correctly | requirements T6 | Unit + System | Solver + API status | Test case design only | Solver; API; status contract | `INFEASIBLE` only with proof; `NO_SOLUTION_FOUND` on timeout without proof | **Blocked** |
| **T7** | Invalid data is rejected with correct code/field; execution stops | requirements T7 | Unit + Contract | Data validator/API | Test case design **yes** | Canonical schema; validation implementation | Validation error payload; no solver run | **Blocked** |
| **T8** | Equal costs break ties by warehouse ID; MILP may return multiple optima | requirements T8 | Unit | Baseline/MILP | Test case design only | Solver; tie-break rule | Deterministic baseline result; valid MILP optima | **Blocked** |
| **T9** | Larger scale records time, status, and solution quality under a time limit | requirements T9 | Performance/System | Solver/API | Test case design only | Solver; scale fixture; timeout config | Runtime, status (including `FEASIBLE`/`NO_SOLUTION_FOUND`), objective/gap, environment | **Blocked** |

---

## 5. Edge-case mapping — EDGE-01 to EDGE-10

Source: [testing-strategy.md §3](../testing-strategy.md).

| Test ID | Edge case | Expected behavior | Level | Preparable now? | Prerequisite | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EDGE-01** | Global stock-out: demand for a SKU exceeds network inventory | `INFEASIBLE` with proof; `NO_SOLUTION_FOUND` if search stopped without proof | System + Invariant | Test data design only | Solver; canonical inventory; status contract | **Blocked** |
| **EDGE-02** | Warehouse bottleneck: nearest warehouse has stock but zero capacity | Divert to secondary warehouse with capacity | Unit + Integration | Test data design only | Solver; capacity fixture | **Blocked** |
| **EDGE-03** | Tight combined capacity and inventory: only a specific complete assignment works | Solver finds the assignment or proves `INFEASIBLE`; no split/unassigned fallback | Unit + System | Test data design only | Solver; tight fixtures (`edge_tight_capacity`, `edge_tight_inventory`) | **Blocked** |
| **EDGE-04** | Zero-demand order | Input validation rejects with documented error (testing-strategy currently says HTTP 400) | Contract | Test case design **yes** | API/schema validation | **Blocked** |
| **EDGE-05** | Equal cost/capacity tie | Deterministic allocation across repeated runs | Unit | Test case design only | Solver; tie-break rule | **Blocked** |
| **EDGE-06** | A route is omitted from `shipping_costs` | Omitted warehouse is never used | Unit + Invariant | Test data design only | Solver; canonical fixture | **Blocked** |
| **EDGE-07** | Only one warehouse has a route and enough stock/capacity | Order is forced to that warehouse | Unit + Integration | Test data design only | Solver; canonical fixture | **Blocked** |
| **EDGE-08** | Time limit reached with no complete solution | `NO_SOLUTION_FOUND`, not `INFEASIBLE` | System | Test case design only | Solver; timeout configuration | **Blocked** |
| **EDGE-09** | Time limit reached after a complete solution | `FEASIBLE` with complete allocations | System | Test case design only | Solver; timeout configuration | **Blocked** |
| **EDGE-10** | Structurally valid but mathematically infeasible dataset | `INFEASIBLE` with proof; dataset remains valid | System + Contract | Test data design **yes** | Canonical fixture; solver/checker | **Blocked** |

> Policy A is decided in [ADR-004](../decisions/0004-allocation-policy-a.md); split-shipment and penalty test cases are not part of the current strategy.

---

## 6. Test data requirements

| Requirement | Needed data | Current state |
| :--- | :--- | :--- |
| Canonical input schema | Warehouse, per-SKU inventory, order, order items, shipping costs | Implemented by TV2: `data/schema/dataset.schema.json` + `docs/data-dictionary.md` |
| Small hand-checkable case | Matches T1/model example | Canonical `data/samples/sample_small.json` (2 warehouses/3 orders/2 SKUs); hand-reviewable but not the same numeric example as the model |
| Feasible case | Enough stock and capacity | Covered by canonical TV2 fixtures; legacy prototype fixture is non-Policy-A |
| Infeasible case | Demand exceeds available resources | `sample_infeasible.json`, `edge_infeasible_stock.json` |
| Tight-resource case | T5 | `edge_tight_capacity.json`, `edge_tight_inventory.json` |
| Tie-break case | T8 | `edge_equal_costs.json` |
| Scale case | T9 | Not identified |
| Invalid-data cases | T7 | Not implemented as fixtures |

TV2 owns dataset generation and schema validation. TV6 will independently verify fixtures against the approved schema; TV6 does not create canonical business data unless the team assigns that work.

---

## 7. Test prerequisites

### 7.1 Required before any acceptance test

- Approved business rules and a single canonical data schema (G0).
- Frozen `ProblemInput`/`SolutionOutput` and API contract (G1).
- Validated fixtures covering T1–T9 and EDGE-01–05 (G2).
- Solver/API modules with documented start commands (G3/G4).
- A dependency manifest and reproducible environment.
- Test evidence format agreed: command, commit SHA, environment, observed output.

### 7.2 Available now

- Python 3.10+ environment (CI uses 3.10; local Python 3.15 observed).
- Repository hygiene checks already in CI.
- Existing JSON fixtures for syntax checks only.
- Requirements/edge-case tables to derive test IDs.

### 7.3 Not available yet

- `pytest` configuration and fixtures.
- Solver, API, database, and frontend implementations.
- Mock API/server for early contract tests.
- CI job that executes tests.

---

## 8. Expected evidence and acceptance criteria

### 8.1 Evidence per test

Every executed test must record:

1. Test ID and requirement/edge-case link.
2. Command and environment.
3. Commit SHA or PR reference.
4. Observed output (pass/fail, status, objective, invariants).
5. For failures: expected vs. actual, reproduction steps, linked bug issue.
6. For benchmarks: dataset version, algorithm, time limit, runtime, status, cost components, utilization.

### 8.2 Entry criteria for acceptance testing

- G0–G4 exit evidence exists.
- Test data is validated and versioned.
- No known P0 business-rule conflict remains.
- CI can run the test suite.

### 8.3 Exit criteria for final acceptance

- **T1–T9:** all executed with recorded evidence; any exception is documented and approved.
- **EDGE-01–10:** all executed, or explicitly deferred with an approved reason per [testing-strategy.md §4](../testing-strategy.md).
- **Invariants:** exactly one warehouse per order, no split/unassigned order, no inventory or capacity violation.
- **API:** contract, validation, infeasibility, and timeout behavior match the approved contract.
- **Persistence:** saved runs reload with identical configuration and metrics.
- **E2E:** dataset selection → solve → results are demonstrated against the live stack.
- **Reproducibility:** same input/configuration produces the documented comparable result.
- **Reporting:** benchmark and final report cite executed evidence, not planned work.

No numeric coverage target is set because the repository does not define one; coverage may be reported as supplementary evidence, not as a substitute for T1–T9/EDGE execution.

---

## 9. Can prepare now vs. must wait

### 9.1 Can prepare now (TV6-owned)

- Traceability matrix maintenance (this document).
- Detailed test-case descriptions for T1–T9 and EDGE-01–05, including expected outcomes from existing requirements.
- Invalid-input test design for T7/EDGE-04.
- CI test-job design (pytest invocation, artifact/report capture).
- Bug-report and verification workflow using existing issue templates.
- Fixture-review checklist for TV2 (schema conformance, expected outcome, version).
- Evidence template and acceptance-report skeleton.
- Repository hygiene checks (JSON syntax, links, `.gitignore` behavior).

### 9.2 Must wait for other modules

- Unit tests for baseline/MILP (TV3).
- Contract tests for solver adapter (TV3) and API (TV5).
- Integration tests for SQLite persistence (TV5).
- System tests for infeasible/timeout behavior (TV3/TV5).
- E2E tests (TV4/TV5).
- Benchmark/performance runs (TV3/TV5).

### 9.3 Requires coordination

- Status enum and error mapping across model, solver, and API.
- Canonical fixture format and edge-case definitions with TV2.
- Mock API availability for TV4 before backend completion.
- Definition of “done” evidence for each handoff in [integration-guide](../integration-guide.md).
- Implementation of the Policy A API contract by TV3/TV4/TV5.

---

## 10. Bug tracking and verification

The repository has issue templates but no issues. Until the Project Lead establishes the issue workflow, TV6 records defects in the test report with:

- Test ID and requirement link.
- Severity: Critical (blocks acceptance), High (blocks a module/gate), Medium (rework), Low (hygiene).
- Reproduction steps, expected vs. actual, environment.
- Verification evidence after fix and the reviewer who confirmed it.

A bug is closed only when the fix is verified by a re-run of the failing test or an equivalent reproducible check.

---

## 11. Traceability maintenance

- Update the matrix whenever TV1 changes requirements or a business rule is approved.
- Link each test ID to a file and test name once the suite exists.
- Do not mark a test as passing based on code review alone.
- If a requirement is removed or changed, mark the affected test IDs as retired and record why.

---

## 12. Related documents

- [Project Status](project-status.md)
- [Task Tracker](task-tracker.md)
- [Integration Plan](integration-plan.md)
- [Requirements](../requirements.md)
- [Testing Strategy](../testing-strategy.md)
- [Integration Guide](../integration-guide.md)
