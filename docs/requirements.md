# Requirements Specification: LogiMind

## 1. Functional Requirements (FR)

| ID | Module / Role | Requirement Description | Status |
| :--- | :--- | :--- | :--- |
| **FR-01** | Data (TV2) | The system shall ingest order, inventory, warehouse capacity, and shipping cost data in standard tabular/JSON formats. | Draft |
| **FR-02** | Optimization (TV3) | The system shall provide a Baseline Heuristic solver that assigns orders based on proximity and single-warehouse availability. | Planned |
| **FR-03** | Optimization (TV3) | The system shall provide a MILP optimization solver that minimizes total cost subject to all inventory and capacity constraints. | Planned |
| **FR-04** | Optimization (TV3) | The system shall output allocation plans detailing warehouse assignments per order line item. | Planned |
| **FR-05** | Optimization (TV3) | The system shall detect and flag infeasible orders (orders that cannot be fulfilled due to stock-out or capacity saturation). | Planned |
| **FR-06** | Backend (TV5) | The backend shall expose REST API endpoints to upload datasets, trigger solver runs, and retrieve allocation metrics. | Planned |
| **FR-07** | Backend (TV5) | The backend shall store problem configurations and solved allocation results in a relational database (SQLite). | Planned |
| **FR-08** | Frontend (TV4) | The frontend shall display warehouse capacity utilization, total cost comparison (Baseline vs. MILP), and split-shipment counts. | Planned |
| **FR-09** | Frontend (TV4) | The frontend shall allow users to inspect order-level routing and view why split shipments occurred. | Planned |
| **FR-10** | Testing (TV6) | The system shall include automated tests validating that no warehouse capacity or inventory limits are violated in any output. | Planned |

---

## 2. Non-Functional Requirements (NFR)

| ID | Category | Requirement Description | Target Metric |
| :--- | :--- | :--- | :--- |
| **NFR-01** | **Correctness** | Zero tolerance for inventory or capacity over-allocation in feasible scenarios. | 100% constraint satisfaction |
| **NFR-02** | **Performance** | Solver execution for a standard test batch (e.g., 500 orders, 5 warehouses, 50 SKUs) must complete within reasonable time. | < 60 seconds (MILP) |
| **NFR-03** | **Reproducibility** | Solver runs on the same input dataset with identical parameters must produce deterministic results. | Deterministic outputs |
| **NFR-04** | **Usability** | The web interface must present cost comparisons and utilization metrics clearly for non-technical evaluators. | Clear UI visual cues |
| **NFR-05** | **Reliability** | API must gracefully return structured validation errors for invalid input payloads without crashing. | Standardized HTTP 4xx/5xx responses |
| **NFR-06** | **Maintainability** | Codebase must adhere to modular separation of concerns between algorithms, backend, and frontend. | Clean architecture separation |

---

## 3. Verification & Acceptance Criteria

1. **Academic Verification:** Mathematical model formulation reviewed and confirmed by TV1 and faculty guidelines.
2. **Algorithmic Verification:** For all test benchmark cases, MILP total cost must be less than or equal to Baseline heuristic cost.
3. **Integration Verification:** TV6 automated test suite passes 100% in CI pipeline on clean environment.
