# Project Overview: LogiMind

## 1. Executive Summary

**LogiMind** is a decision-support system for the Multi-Warehouse Order Allocation
Problem (MWOAP). Customer orders must be routed to fulfillment warehouses based on
per-SKU stock availability, warehouse processing capacity, and shipping cost.

LogiMind formulates this problem as a Mixed-Integer Linear Program (MILP),
compares the optimal allocation with baseline heuristic rules, and presents the
results through a web application for supply chain operators.

The canonical allocation policy is **Policy A — Strict Non-Split Allocation**
([ADR-004](decisions/0004-allocation-policy-a.md)):

- every order is fulfilled completely;
- every order is assigned to exactly one warehouse;
- split shipments are not allowed;
- unassigned orders are not allowed;
- there is no split penalty, unassigned penalty, or handling cost;
- warehouse capacity is measured in **number of orders**;
- inventory is tracked **per SKU**;
- the objective minimizes total shipping cost.

If no complete allocation exists, the instance is **mathematically infeasible**;
the dataset is still structurally valid.

---

## 2. Business Context & Motivation

E-commerce businesses operate multiple fulfillment centers to reduce delivery
distances. Multi-warehouse operations introduce these trade-offs:

1. **Stock Fragmentation:** An order containing several SKUs may not be fully
   available at the nearest warehouse.
2. **Single-Warehouse Fulfillment:** Policy A requires the whole order to ship
   from one warehouse, so a warehouse is eligible only if it holds all required
   SKU quantities.
3. **Capacity Bottlenecks:** Directing all orders to the closest warehouse can
   exhaust its order-processing capacity and force later orders onto more
   expensive routes.
4. **Shipping Cost vs. Capacity:** A cheaper warehouse may have no capacity or
   stock, so the solver must consider the whole batch rather than choosing the
   nearest warehouse independently for each order.

LogiMind balances these factors to minimize total shipping cost while respecting
per-SKU inventory and order-count capacity. Split shipments, handling fees, and
unassigned penalties are outside the current policy and are not optimized.

---

## 3. Core Objectives

1. **Model Formulation:** Implement the Policy A MILP model in
   [docs/mathematical-model.md](mathematical-model.md).
2. **Benchmarking:** Compare a deterministic baseline heuristic with the MILP on
   identical canonical datasets and report total shipping cost, assigned orders,
   utilization, and runtime.
3. **Data Realism:** Provide reproducible synthetic datasets under
   `data/samples/`, validated against
   [data/schema/dataset.schema.json](../data/schema/dataset.schema.json).
4. **Interactive Visualization:** Let operators select a dataset, run an
   allocation, and inspect one warehouse per order, cost, and capacity usage.
5. **Academic Rigor:** Maintain reproducibility, automated tests, and one
   authoritative data contract.

---

## 4. Project Scope

### In Scope

- Multi-warehouse order assignment within one fulfillment planning window.
- Single-SKU and multi-SKU orders.
- Per-SKU inventory and order-count warehouse capacity.
- Precomputed order–warehouse shipping costs.
- Policy A statuses: `OPTIMAL`, `FEASIBLE`, `INFEASIBLE`, `NO_SOLUTION_FOUND`,
  `ERROR`.
- Comparison metrics: total shipping cost, assigned orders, warehouse
  utilization, and computation time.

### Out of Scope (Deferred)

- Split shipments, handling fees, and unassigned-order penalties (not part of
  Policy A).
- Real-time fleet vehicle routing and turn-by-turn navigation.
- Long-term inventory replenishment and demand forecasting.
- Dynamic pricing and carrier API negotiation.

---

## 5. Authoritative Documents

| Topic | Document |
| :--- | :--- |
| Mathematical model | [mathematical-model.md](mathematical-model.md) |
| Requirements | [requirements.md](requirements.md) |
| Dataset contract | [data-dictionary.md](data-dictionary.md) |
| API interface | [api-contract.md](api-contract.md) |
| Testing methodology | [testing-strategy.md](testing-strategy.md) |
| Policy decision | [ADR-004](decisions/0004-allocation-policy-a.md) |
