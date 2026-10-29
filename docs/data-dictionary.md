# Data Dictionary: LogiMind

> **Primary Owner:** TV2 (Data & Test Dataset)  
> **Status:** Baseline Specification (Draft)

---

## 1. Entities Overview

The LogiMind data model models four core domain entities and one execution result entity:
1. **Warehouse (`warehouses`):** Fulfillment facilities with location and capacity properties.
2. **SKU (`skus`):** Product catalog items with dimensions/weights.
3. **Inventory (`inventory`):** Stock levels of specific SKUs at specific warehouses.
4. **Order (`orders` & `order_lines`):** Customer demands with destination and SKU quantities.
5. **Shipping Cost Matrix (`shipping_rates`):** Transportation cost mapping warehouse $\to$ destination/order.
6. **Allocation Result (`allocation_runs` & `allocations`):** Solver output records.

---

## 2. Entity Specifications

### 2.1 Warehouse (`warehouses`)

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `warehouse_id` | String | Yes | Primary Key (e.g. `WH-01`) | Unique warehouse identifier |
| `name` | String | Yes | Non-empty | Human-readable facility name |
| `location_code`| String | Yes | Non-empty | Geographic zone or postal code |
| `daily_capacity`| Integer| Yes | $> 0$ | Max throughput (units or orders per day) |
| `handling_cost_per_unit` | Float | No | $\ge 0$, Default: 0.50 | Handling fee per item processed |

---

### 2.2 SKU (`skus`)

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `sku_id` | String | Yes | Primary Key (e.g. `SKU-1001`) | Unique stock keeping unit code |
| `name` | String | Yes | Non-empty | Product name |
| `weight_kg` | Float | No | $> 0$ | Unit weight for shipping calculation |
| `volume_cbm` | Float | No | $> 0$ | Unit volume in cubic meters |

---

### 2.3 Inventory (`inventory`)

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `warehouse_id` | String | Yes | FK $\to$ `warehouses.warehouse_id` | Warehouse holding the stock |
| `sku_id` | String | Yes | FK $\to$ `skus.sku_id` | Stocked product identifier |
| `quantity_on_hand` | Integer | Yes | $\ge 0$ | Available unreserved stock |

*Composite Primary Key: (`warehouse_id`, `sku_id`)*

---

### 2.4 Order & Order Lines

#### Order Header (`orders`)
| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | String | Yes | Primary Key (e.g. `ORD-5001`) | Unique order identifier |
| `customer_zone`| String | Yes | Non-empty | Delivery destination region |
| `created_at` | DateTime | Yes | ISO 8601 | Timestamp of order receipt |

#### Order Line Item (`order_lines`)
| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | String | Yes | FK $\to$ `orders.order_id` | Parent order reference |
| `sku_id` | String | Yes | FK $\to$ `skus.sku_id` | Demanded item identifier |
| `quantity` | Integer | Yes | $> 0$ | Number of units ordered |

*Composite Primary Key: (`order_id`, `sku_id`)*

---

### 2.5 Shipping Rate Matrix (`shipping_rates`)

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `warehouse_id` | String | Yes | FK $\to$ `warehouses.warehouse_id` | Origin warehouse |
| `destination_zone` | String | Yes | Non-empty | Destination delivery zone |
| `base_cost` | Float | Yes | $\ge 0$ | Fixed shipment cost |
| `cost_per_kg` | Float | No | $\ge 0$ | Weight-based increment |

---

## 3. Storage Formats

- **Persistent Relational DB:** SQLite schema mirroring the tables above.
- **Fixture Files for Testing:** JSON and CSV formats stored in `data/samples/`.
