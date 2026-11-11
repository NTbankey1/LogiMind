# ADR-004: Adoption of Policy A as the Canonical Order Allocation Policy

## Status
ACCEPTED

## Date
2026-11-11

## Decision Owner
Project Lead & TV2 (Data & Test Dataset)

## Context
LogiMind initially explored two operational allocation policies:
- **Policy A (Strict Non-Split Allocation):** Every order must be assigned to exactly one warehouse and fulfilled in full. Each warehouse has an order processing capacity (number of orders) and per-SKU inventory. The objective minimizes total shipping costs with no unassigned orders permitted.
- **Policy B (Penalty-Based Allocation with Unassigned Orders):** Allows orders to remain unassigned at a cost penalty or allows partial fulfillment/split shipment with additional penalties.

The early mathematical draft and prototype fixtures contained conflicting definitions, mixing fields from Policy B (`split_penalty`, `unassigned_penalty`, `handling_cost_per_unit`, `daily_capacity`) with basic assignments.

To establish an authoritative, unambiguous data contract and operational objective for baseline heuristics (TV3), MILP formulation (TV3), API endpoints (TV5), and test evaluation (TV6), the Project Lead explicitly selected **Policy A**.

## Decision
LogiMind formally adopts **Policy A** as the canonical fulfillment policy for all production datasets, optimization algorithms, API schemas, and validation pipelines:

1. **Atomic Order Allocation:** Every order is fulfilled completely by exactly one warehouse. Splitting an order across multiple warehouses is strictly prohibited.
2. **Complete Fulfillment Requirement:** Every order in a dataset must be assigned. There is no unassigned-order decision variable, unassigned penalty, or split penalty in the objective function.
3. **Objective Function:** Minimize total transportation cost across all assigned order-warehouse pairs:
   $$\min \sum_{i \in I} \sum_{j \in J} c_{ij} x_{ij}$$
   where $x_{ij} \in \{0, 1\}$ indicates assignment of order $i$ to warehouse $j$, and $c_{ij}$ is the shipping cost.
4. **Order Processing Capacity:** Warehouse throughput capacity (`capacity_orders`) is measured strictly in the number of discrete orders processed, not product item units.
5. **Per-SKU Inventory:** Stock is tracked individually per SKU at each warehouse. An assigned order consumes its required item quantities directly from that warehouse's inventory.
6. **Route Availability:** Order-warehouse delivery routes are defined explicitly in `shipping_costs`. If a warehouse is omitted from an order's `shipping_costs` map, that delivery route is unavailable.

## Consequences

- **Positive:**
  - Clear, unambiguous mathematical model: integer linear program with standard generalized assignment / facility allocation structure.
  - Strict data contract enforceable via JSON Schema Draft 2020-12 and semantic validation.
  - Consistent benchmarks for TV3 (MILP solver), TV5 (FastAPI backend), and TV6 (frontend/reporting).
  - Clear separation between dataset validity (conforming to schema and semantic rules) and mathematical feasibility (existence of a resource-compliant allocation).
- **Negative / Risks:**
  - Instances can be structurally valid but mathematically infeasible if warehouse capacities or inventories are insufficient.
  - Solvers must prove infeasibility rather than defaulting to leaving orders unassigned.
- **Interface Impacts:**
  - TV2 schema and fixtures are standardized on Policy A.
  - Legacy `benchmark_data.json` is retained solely for historical prototype compatibility and documented as legacy.
