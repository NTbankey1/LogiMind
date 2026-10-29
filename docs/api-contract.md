# API Contract Specification: LogiMind

> **Status:** Proposed Specification (Pending TV4, TV5, and TV3 sign-off)  
> **Base URL:** `/api/v1`  
> **Format:** `application/json`

---

## 1. Overview & Protocol Guidelines

This contract defines the integration interface between:
- **Frontend Client (TV4)** and **Backend Service (TV5)**
- **Backend Service (TV5)** and **Optimization Solver Engine (TV3)**

All timestamps use ISO 8601 UTC format (e.g., `2026-10-29T08:00:00Z`). All currency amounts are represented as floats rounded to 2 decimal places.

---

## 2. Standard Response & Error Envelope

All API responses follow a consistent envelope structure:

### Success Envelope
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed successfully",
  "timestamp": "2026-10-29T08:00:00Z"
}
```

### Error Envelope
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid warehouse capacity or negative demand",
    "details": [
      {
        "field": "warehouses[0].capacity",
        "issue": "Capacity must be greater than zero"
      }
    ]
  },
  "timestamp": "2026-10-29T08:00:00Z"
}
```

---

## 3. Endpoints [Proposed]

### 3.1 Health & System Information

#### `GET /api/v1/health`
- **Purpose:** Verifies backend health and solver engine readiness.
- **Response:**
```json
{
  "success": true,
  "data": {
    "status": "UP",
    "version": "0.1.0",
    "solver_backend": "PuLP / CBC",
    "database": "connected"
  }
}
```

---

### 3.2 Dataset Management

#### `GET /api/v1/datasets`
- **Purpose:** Lists available test datasets (seeded by TV2).
- **Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "ds-sample-small",
      "name": "Small Benchmark (5 Warehouses, 50 Orders)",
      "num_warehouses": 5,
      "num_orders": 50,
      "num_skus": 10
    }
  ]
}
```

---

### 3.3 Trigger Optimization Run

#### `POST /api/v1/allocations/run`
- **Purpose:** Submits an order batch to be solved by the designated algorithm.
- **Request Headers:** `Content-Type: application/json`
- **Request Body Schema:**
```json
{
  "dataset_id": "ds-sample-small",
  "algorithm": "MILP",
  "parameters": {
    "time_limit_seconds": 60,
    "allow_split_shipments": true,
    "split_penalty": 15.0
  }
}
```

*(Alternatively, inline payload supporting ad-hoc datasets):*
```json
{
  "algorithm": "BASELINE",
  "warehouses": [
    {
      "id": "WH-01",
      "name": "Northern Hub",
      "capacity": 100,
      "inventory": { "SKU-A": 50, "SKU-B": 30 }
    }
  ],
  "orders": [
    {
      "id": "ORD-101",
      "destination": "Zone-A",
      "items": { "SKU-A": 2, "SKU-B": 1 },
      "shipping_costs": { "WH-01": 5.5 }
    }
  ],
  "parameters": {
    "split_penalty": 10.0
  }
}
```

- **Response Body (200 OK):**
```json
{
  "success": true,
  "data": {
    "run_id": "run-20261029-001",
    "algorithm": "MILP",
    "status": "OPTIMAL",
    "summary": {
      "total_cost": 1245.50,
      "shipping_cost": 890.00,
      "handling_cost": 310.50,
      "split_penalty_cost": 45.00,
      "total_orders": 50,
      "fulfilled_orders": 50,
      "split_orders_count": 3,
      "solve_time_seconds": 1.42
    },
    "warehouse_utilization": [
      {
        "warehouse_id": "WH-01",
        "used_capacity": 85,
        "max_capacity": 100,
        "utilization_pct": 85.0
      }
    ],
    "allocations": [
      {
        "order_id": "ORD-101",
        "is_split": false,
        "lines": [
          {
            "sku": "SKU-A",
            "quantity": 2,
            "fulfilled_by": "WH-01"
          },
          {
            "sku": "SKU-B",
            "quantity": 1,
            "fulfilled_by": "WH-01"
          }
        ]
      }
    ]
  }
}
```

---

### 3.4 Algorithm Benchmarking (Comparison)

#### `POST /api/v1/allocations/compare`
- **Purpose:** Executes both `BASELINE` and `MILP` on the identical dataset and returns side-by-side metrics.
- **Request Body:**
```json
{
  "dataset_id": "ds-sample-small"
}
```
- **Response Body:**
```json
{
  "success": true,
  "data": {
    "baseline": {
      "total_cost": 1580.00,
      "split_orders": 12,
      "solve_time_seconds": 0.05
    },
    "milp": {
      "total_cost": 1245.50,
      "split_orders": 3,
      "solve_time_seconds": 1.42
    },
    "comparison": {
      "cost_savings_pct": 21.17,
      "split_reduction_count": 9
    }
  }
}
```

---

## 4. Timeout & Solver Failure Handling

1. **Solver Timeouts:** If the solver fails to find a verified optimal within `time_limit_seconds`, it must return the best feasible integer solution found so far with status `"FEASIBLE_SUBOPTIMAL"`.
2. **Infeasibility:** If total order demand exceeds global network inventory, the solver returns status `"INFEASIBLE"` (or `"PARTIALLY_FULFILLED"` if unassigned slack is permitted), accompanied by a list of unsatisfied order IDs.
3. **HTTP Status Codes:**
   - `200 OK`: Successful computation.
   - `400 Bad Request`: Schema validation failure or negative values.
   - `422 Unprocessable Entity`: Mathematically infeasible instance when slack is disabled.
   - `504 Gateway Timeout`: Solver calculation exceeded server timeout boundary.
