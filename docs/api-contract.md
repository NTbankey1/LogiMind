# API Contract Specification: LogiMind

> **Status:** Policy A aligned (2026-11-11). Pending TV3/TV4/TV5 implementation sign-off.
> **Base URL:** `/api/v1`
> **Format:** `application/json`
> **Canonical dataset contract:** [`data/schema/dataset.schema.json`](../data/schema/dataset.schema.json) and [`docs/data-dictionary.md`](data-dictionary.md)

This is the **only** API data contract. It must not introduce fields that are
absent from the canonical Policy A schema.

---

## 1. Scope and protocol

This contract defines:

- **TV4 → TV5:** request/response payloads for dataset listing and allocation runs.
- **TV5 → TV3:** the solver input (`dataset`) and solver result (`status`,
  `allocations`, metrics).

All timestamps are ISO 8601 UTC. Shipping costs are finite, non-negative numbers;
currency units are dataset-defined but must be consistent within a dataset.

### Policy A rules enforced by this contract

1. Every order is assigned to exactly one warehouse.
2. Every order is fulfilled completely.
3. Split shipments are not allowed.
4. Unassigned orders are not allowed.
5. There is no split penalty, unassigned penalty, or handling cost.
6. Warehouse capacity is measured in **orders** (`capacity_orders`).
7. Inventory is tracked **per SKU** at each warehouse.
8. The objective is total shipping cost.
9. A structurally valid dataset may be mathematically infeasible.
10. `INFEASIBLE` may only be reported with a proof (exhaustive search or solver
    infeasibility certificate). A timeout without a solution is
    `NO_SOLUTION_FOUND`, not `INFEASIBLE`.

---

## 2. Canonical dataset payload

A dataset request body or stored dataset must validate against
[`data/schema/dataset.schema.json`](../data/schema/dataset.schema.json):

| Entity | Fields used by the API |
| :--- | :--- |
| Dataset | `schema_version`, `dataset_id`, `name`, `description`, `policy`, `skus`, `warehouses`, `orders`, optional `metadata` |
| SKU | `sku_id`, `name` |
| Warehouse | `warehouse_id`, `name`, `capacity_orders`, `inventory` (`sku_id → integer stock ≥ 0`) |
| Order | `order_id`, `items` (`sku_id → positive integer`), `shipping_costs` (`warehouse_id → finite cost ≥ 0`) |

**Capacity unit:** `capacity_orders` is a number of orders, never item units.
**Inventory:** every warehouse must declare every SKU; missing keys are invalid,
zero means unavailable.
**Routes:** an omitted warehouse key in `shipping_costs` means the route is
unavailable; it is not a zero cost.

### 2.1 Inline dataset example

```json
{
  "schema_version": "1.0",
  "dataset_id": "sample-small",
  "name": "Small Feasible Benchmark",
  "description": "2 warehouses, 3 orders, 2 SKUs",
  "policy": "A",
  "skus": [
    { "sku_id": "SKU-A", "name": "Product Alpha" },
    { "sku_id": "SKU-B", "name": "Product Beta" }
  ],
  "warehouses": [
    {
      "warehouse_id": "WH-01",
      "name": "Warehouse North",
      "capacity_orders": 2,
      "inventory": { "SKU-A": 10, "SKU-B": 5 }
    },
    {
      "warehouse_id": "WH-02",
      "name": "Warehouse South",
      "capacity_orders": 2,
      "inventory": { "SKU-A": 5, "SKU-B": 10 }
    }
  ],
  "orders": [
    {
      "order_id": "ORD-001",
      "items": { "SKU-A": 2, "SKU-B": 1 },
      "shipping_costs": { "WH-01": 4.0, "WH-02": 8.0 }
    },
    {
      "order_id": "ORD-002",
      "items": { "SKU-A": 3 },
      "shipping_costs": { "WH-01": 5.0, "WH-02": 7.0 }
    },
    {
      "order_id": "ORD-003",
      "items": { "SKU-B": 4 },
      "shipping_costs": { "WH-01": 9.0, "WH-02": 3.0 }
    }
  ]
}
```

---

## 3. Standard response and error envelopes

### Success envelope

```json
{
  "success": true,
  "data": { },
  "message": "Operation completed successfully",
  "timestamp": "2026-11-11T08:00:00Z"
}
```

### Error envelope

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Dataset failed Policy A validation",
    "details": [
      { "field": "warehouses[0].inventory.SKU-B", "issue": "Missing inventory entry" }
    ]
  },
  "timestamp": "2026-11-11T08:00:00Z"
}
```

Error and outcome codes:

| Code | Meaning | HTTP |
| :--- | :--- | :--- |
| `VALIDATION_ERROR` | Request or dataset violates the canonical schema/semantic rules. | `400` |
| `INFEASIBLE` | Valid dataset; no complete Policy A allocation exists, **proven**. | `422` |
| `SOLVER_ERROR` | Solver/model execution failed unexpectedly. | `500` |
| `NO_SOLUTION_FOUND` | Search stopped (for example timeout) without a solution and without an infeasibility proof. Returned as a normal run status, not an error envelope. | `200` |

---

## 4. Endpoints

### 4.1 `GET /api/v1/health`

```json
{
  "success": true,
  "data": {
    "status": "UP",
    "version": "0.1.0",
    "solver_backend": "PuLP / CBC",
    "database": "connected"
  },
  "timestamp": "2026-11-11T08:00:00Z"
}
```

### 4.2 `GET /api/v1/datasets`

Lists stored canonical datasets. Response items contain metadata only; use the
detail endpoint for the full dataset.

```json
{
  "success": true,
  "data": [
    {
      "dataset_id": "sample-small",
      "name": "Small Feasible Benchmark",
      "policy": "A",
      "num_warehouses": 2,
      "num_orders": 3,
      "num_skus": 2
    }
  ],
  "timestamp": "2026-11-11T08:00:00Z"
}
```

### 4.3 `GET /api/v1/datasets/{dataset_id}`

Returns the full canonical dataset object from §2.

### 4.4 `POST /api/v1/allocations/run`

Exactly one of `dataset_id` or `dataset` is required.

**Request with a stored dataset:**

```json
{
  "dataset_id": "sample-small",
  "algorithm": "MILP",
  "parameters": {
    "time_limit_seconds": 60,
    "seed": 20261111
  }
}
```

**Request with an inline canonical dataset:**

```json
{
  "dataset": { "schema_version": "1.0", "dataset_id": "inline-example", "name": "Inline Policy A Example", "description": "Single warehouse, single order", "policy": "A", "skus": [{ "sku_id": "SKU-A", "name": "Product Alpha" }], "warehouses": [{ "warehouse_id": "WH-01", "name": "Warehouse North", "capacity_orders": 1, "inventory": { "SKU-A": 10 } }], "orders": [{ "order_id": "ORD-001", "items": { "SKU-A": 2 }, "shipping_costs": { "WH-01": 4.0 } }] },
  "algorithm": "BASELINE",
  "parameters": {
    "time_limit_seconds": 30
  }
}
```

`dataset` must validate against the canonical schema. `algorithm` is
`BASELINE` or `MILP`. `parameters.time_limit_seconds` is a positive number;
`parameters.seed` is an optional integer used for deterministic tie-breaking.
There are no split, penalty, or handling parameters.

**Successful response (`200 OK`):**

```json
{
  "success": true,
  "data": {
    "run_id": "run-20261111-001",
    "dataset_id": "sample-small",
    "policy": "A",
    "algorithm": "MILP",
    "status": "OPTIMAL",
    "termination_reason": "OPTIMALITY_PROVEN",
    "summary": {
      "total_orders": 3,
      "assigned_orders": 3,
      "shipping_cost": 12.0,
      "objective_value": 12.0,
      "solve_time_seconds": 0.12
    },
    "warehouse_utilization": [
      {
        "warehouse_id": "WH-01",
        "used_capacity_orders": 2,
        "capacity_orders": 2,
        "utilization_pct": 100.0
      },
      {
        "warehouse_id": "WH-02",
        "used_capacity_orders": 1,
        "capacity_orders": 2,
        "utilization_pct": 50.0
      }
    ],
    "allocations": [
      { "order_id": "ORD-001", "warehouse_id": "WH-01", "shipping_cost": 4.0 },
      { "order_id": "ORD-002", "warehouse_id": "WH-01", "shipping_cost": 5.0 },
      { "order_id": "ORD-003", "warehouse_id": "WH-02", "shipping_cost": 3.0 }
    ]
  },
  "timestamp": "2026-11-11T08:00:00Z"
}
```

Response rules:

- `allocations` has exactly one entry per order; each entry has exactly one
  `warehouse_id`.
- `summary.assigned_orders` equals `summary.total_orders` for any
  `OPTIMAL` or `FEASIBLE` result.
- `summary.shipping_cost` equals `summary.objective_value`; there is no
  handling cost or penalty component.
- `warehouse_utilization[].used_capacity_orders` counts orders, not units.
- There is no `is_split`, `lines[].fulfilled_by`, `split_orders_count`,
  `handling_cost`, `split_penalty_cost`, or unassigned-order field.

### 4.5 `POST /api/v1/allocations/compare`

Runs `BASELINE` and `MILP` on the identical canonical dataset.

**Request:**

```json
{
  "dataset_id": "sample-small",
  "parameters": { "time_limit_seconds": 60 }
}
```

**Response (`200 OK`):**

```json
{
  "success": true,
  "data": {
    "dataset_id": "sample-small",
    "policy": "A",
    "baseline": {
      "status": "FEASIBLE",
      "shipping_cost": 12.0,
      "assigned_orders": 3,
      "solve_time_seconds": 0.01
    },
    "milp": {
      "status": "OPTIMAL",
      "shipping_cost": 12.0,
      "assigned_orders": 3,
      "solve_time_seconds": 0.12
    },
    "comparison": {
      "cost_savings_absolute": 0.0,
      "cost_savings_pct": 0.0
    }
  },
  "timestamp": "2026-11-11T08:00:00Z"
}
```

When baseline cannot find a complete allocation, it returns `status:
"NO_SOLUTION_FOUND"` (or `INFEASIBLE` only with proof). Comparison metrics are
`null` when either side has no complete solution; no split metric is reported.

The numbers above are illustrative for `sample-small`; on that fixture the
baseline and MILP can both reach 12.0. They are not a benchmark claim. TV6 owns
comparative performance evidence.

---

## 5. Solver status semantics and timeout handling

| Status | Meaning | HTTP |
| :--- | :--- | :--- |
| `OPTIMAL` | A complete valid Policy A allocation was found and proven optimal. | `200` |
| `FEASIBLE` | A complete valid allocation was found, but optimality was not proven (for example, time limit reached). | `200` |
| `INFEASIBLE` | A valid dataset; no complete allocation exists, with a proof/certificate. | `422` |
| `NO_SOLUTION_FOUND` | Search stopped without a complete solution and without an infeasibility proof. **Never** report this as `INFEASIBLE`. | `200` |
| `ERROR` | Invalid input or unexpected execution failure. | `400` / `500` |

Timeout rules:

1. If the time limit is reached **after** a complete valid allocation is found,
   return `200` with `status: "FEASIBLE"` and
   `termination_reason: "TIME_LIMIT"`.
2. If the time limit is reached **without** a complete solution and without an
   infeasibility proof, return `200` with `status: "NO_SOLUTION_FOUND"` and an
   empty `allocations` list.
3. Return `INFEASIBLE` only when exhaustive search or the solver proves that no
   complete allocation exists. A timeout is never proof.
4. `504 Gateway Timeout` is reserved for infrastructure/network timeouts, not for
   a solver reaching its configured time limit.

Input validation errors use HTTP `400` with `VALIDATION_ERROR` and field-level
details. A mathematically infeasible but structurally valid dataset uses HTTP
`422` with `INFEASIBLE`; the two must never be conflated.

`termination_reason` is a string such as `OPTIMALITY_PROVEN`, `TIME_LIMIT`,
`INFEASIBILITY_PROVEN`, or `SEARCH_LIMIT`. It explains why the solver stopped and
must be consistent with `status`.

---

## 6. TV1–TV6 integration mapping

| Component | Data source | Policy A rules to follow |
| :--- | :--- | :--- |
| **TV1** | `docs/mathematical-model.md` | Full fulfillment, exactly one warehouse per order, no split, no unassigned variable, shipping-cost-only objective. |
| **TV2** | `data/schema/dataset.schema.json`, `docs/data-dictionary.md` | Canonical field names, complete per-SKU inventory, order-count capacity, finite non-negative shipping costs, route omission means unavailable. |
| **TV3** | Canonical dataset (`dataset` payload) | Return one warehouse per order; enforce per-SKU stock and `capacity_orders`; report `OPTIMAL`/`FEASIBLE`/`INFEASIBLE`/`NO_SOLUTION_FOUND`/`ERROR` accurately. |
| **TV4** | API responses in §4 | Display exactly one warehouse per order, order-count utilization, and shipping cost only; no split or penalty views. |
| **TV5** | API request/response and canonical schema | Validate every inline/stored dataset against the canonical schema before solving; preserve the status and error distinctions in §5. |
| **TV6** | API contract and testing strategy | Verify one-warehouse-per-order, per-SKU stock, order-count capacity, cost recomputation, status semantics, and infeasibility-vs-timeout behavior. |

### 6.1 Field/unit consistency checklist

| Item | Canonical value |
| :--- | :--- |
| Warehouse ID field | `warehouse_id` (not `id`) |
| Capacity field/unit | `capacity_orders`, measured in orders |
| Inventory field | `inventory` map on each warehouse, complete for every SKU |
| Order ID field | `order_id` |
| Demand field | `items` map, positive integer quantities |
| Cost field | `shipping_costs` map, finite non-negative cost per available warehouse |
| Unavailable route | Warehouse key omitted from `shipping_costs` |
| Inventory stock | Integer `>= 0`; zero means unavailable |
| Objective | Total shipping cost only |
| Allocation response | One `warehouse_id` per `order_id` |

Any implementation that uses different names, item-unit capacity, penalty
fields, split allocations, or a different status vocabulary is non-conforming
and must be updated by its owning role (TV3/TV4/TV5).
