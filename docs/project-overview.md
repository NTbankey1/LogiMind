# Project Overview: LogiMind

## 1. Executive Summary

**LogiMind** is an intelligent decision-support system designed to solve the Multi-Warehouse Order Allocation Problem (MWOAP). In modern logistics and e-commerce fulfillment networks, customer orders must be routed to appropriate fulfillment centers based on stock availability, processing limits, transportation costs, and split-shipment trade-offs.

LogiMind formulates this problem as a Mixed-Integer Linear Program (MILP), compares optimal allocations against baseline heuristic rules, and presents the results through an intuitive web application for supply chain operators.

---

## 2. Business Context & Motivation

E-commerce businesses typically operate multiple fulfillment centers (regional warehouses) to reduce last-mile delivery distances. However, multi-warehouse operations introduce complex trade-offs:
1. **Stock Fragmentation:** A single customer order containing multiple items may not be fully available at the nearest warehouse.
2. **Split Shipment Costs:** Fulfilling an order from two or more warehouses multiplies packaging, handling, and delivery fees while degrading customer experience.
3. **Capacity Bottlenecks:** Directing all orders to the closest warehouse quickly exceeds its daily picking and packing throughput limit.
4. **Distance vs. Handling Fees:** A distant warehouse with excess capacity may be cheaper to handle than a strained local warehouse, but shipping costs are higher.

LogiMind balances these factors systematically to minimize overall fulfillment expense while respecting physical logistics constraints.

---

## 3. Core Objectives

1. **Model Formulation:** Develop a mathematically rigorous MILP model reflecting real-world warehouse logistics.
2. **Benchmarking:** Implement standard baseline heuristics (e.g., nearest-first greedy assignment) to quantify cost reduction delivered by MILP.
3. **Data Realism:** Provide synthetic datasets representing realistic order distributions, warehouse networks, and SKU catalogs.
4. **Interactive Visualization:** Provide an accessible web interface for operators to upload batches, inspect allocations, and analyze cost breakdowns.
5. **Academic Rigor:** Structure the system with full reproducibility, comprehensive automated tests, and clear documentation.

---

## 4. Project Scope

### In-Scope
- Multi-warehouse order assignment within a single fulfillment planning window (e.g., daily batch).
- Single-SKU and multi-SKU orders.
- Fixed handling costs, variable shipping costs, and split-shipment penalties.
- Comparison metrics: Total Cost, Number of Split Orders, Warehouse Utilization Rate, Computation Time.

### Out-of-Scope (Deferred to Future Work)
- Real-time fleet vehicle routing and turn-by-turn road navigation.
- Long-term inventory replenishment and demand forecasting.
- Dynamic pricing and carrier API contract negotiation.
