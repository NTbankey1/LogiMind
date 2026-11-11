# Data Dictionary: LogiMind Policy A Datasets

> **Primary Owner:** TV2 (Data & Test Dataset)
> **Status:** Canonical
> **Machine-readable schema:** [`data/schema/dataset.schema.json`](../data/schema/dataset.schema.json)
> **Policy decision:** [ADR-004: Adoption of Policy A](decisions/0004-allocation-policy-a.md)

This document is the single authoritative description of the LogiMind benchmark
dataset contract. Any other dataset description in the repository is either a
deprecation pointer or a legacy artifact documented in
[Legacy artifacts](#10-legacy-artifacts).

---

## 1. Allocation policy (Policy A)

The Project Lead selected **Policy A** as the canonical allocation policy. Every
valid dataset therefore describes an *atomic, complete* assignment problem:

1. Each order is assigned to **exactly one** warehouse.
2. Orders are **never split** across warehouses.
3. Every order must be fulfilled **completely**.
4. Warehouse capacity is measured in **number of orders**, not product units.
5. Inventory is tracked **per SKU, per warehouse**.
6. An assigned order consumes all of its requested SKU quantities from its one
   warehouse.
7. A chosen order–warehouse assignment must have a **shipping cost** in the
   dataset; an omitted warehouse means the route is unavailable.
8. The objective is to minimize total shipping cost:
   `minimize sum(shipping_cost[order_id][warehouse_id])`.
9. There is no unassigned-order variable.
10. There is no unassigned penalty, split penalty, or handling-cost field.

Policy B (penalty-based, split/unassigned orders) is retained only as historical
documentation in `docs/mathematical-model.md` §3 and `docs/requirements.md`. It is
**not** part of this contract.

---

## 2. Dataset structure

Datasets are UTF-8 JSON documents shaped as follows:

```json
{
  "schema_version": "1.0",
  "dataset_id": "sample-small",
  "name": "Small Feasible Dataset",
  "description": "A small Policy A benchmark.",
  "policy": "A",
  "skus": [
    { "sku_id": "SKU-A", "name": "Product A" }
  ],
  "warehouses": [
    {
      "warehouse_id": "WH-01",
      "name": "Warehouse 1",
      "capacity_orders": 2,
      "inventory": { "SKU-A": 10 }
    }
  ],
  "orders": [
    {
      "order_id": "ORD-001",
      "items": { "SKU-A": 3 },
      "shipping_costs": { "WH-01": 5.0 }
    }
  ],
  "metadata": {
    "generator": "LogiMind TV2 dataset generator",
    "seed": 20261111
  }
}
```

---

## 3. Top-level fields

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `schema_version` | String | Yes | Exactly `"1.0"` | Contract version. Unsupported values are rejected. |
| `dataset_id` | String | Yes | Non-empty, unique per file | Stable dataset identifier. |
| `name` | String | Yes | Non-empty | Human-readable dataset name. |
| `description` | String | Yes | Non-empty | Scenario description, including expected feasibility. |
| `policy` | String | Yes | Exactly `"A"` | Allocation policy. Policy B is rejected. |
| `skus` | Array | Yes | At least 1 item | SKU catalogue. |
| `warehouses` | Array | Yes | At least 1 item | Warehouse list with capacity and full inventory. |
| `orders` | Array | Yes | At least 1 item | Orders to allocate. |
| `metadata` | Object | No | — | Reproducibility information (generator, seed, notes). |

Unknown top-level fields are rejected (`additionalProperties: false`).

---

## 4. Entity fields

### 4.1 SKU (`skus[]`)

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `sku_id` | String | Yes | Non-empty, unique across `skus` | Primary key for the product. |
| `name` | String | Yes | Non-empty | Human-readable product name. |

### 4.2 Warehouse (`warehouses[]`)

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `warehouse_id` | String | Yes | Non-empty, unique across `warehouses` | Primary key for the facility. |
| `name` | String | Yes | Non-empty | Human-readable facility name. |
| `capacity_orders` | Integer | Yes | `>= 0`; booleans rejected | Maximum number of **orders** this warehouse can process in the batch. |
| `inventory` | Object | Yes | At least 1 entry; every known SKU exactly once | Map `sku_id -> integer stock >= 0`. |

`inventory` is **complete by contract**: every warehouse must declare every SKU in
`skus`, including SKUs it cannot supply. Use `0` for unavailable stock; a missing
key is a validation error, not an implicit zero.

### 4.3 Order (`orders[]`)

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | String | Yes | Non-empty, unique across `orders` | Primary key for the order. |
| `items` | Object | Yes | At least 1 entry; known SKUs; integer quantity `>= 1` | Map `sku_id -> units required`. |
| `shipping_costs` | Object | Yes | Known warehouses; finite number `>= 0` | Map `warehouse_id -> cost of shipping the whole order from that warehouse`. |

Semantics:

- An **omitted** warehouse key in `shipping_costs` means the route is
  unavailable for that order. It is not a zero cost.
- A shipping cost of **`0` is valid** and means a genuinely free route.
- Each order must be shipped whole from one warehouse; `items` is not split.

---

## 5. Units and interpretation

| Concept | Unit | Notes |
| :--- | :--- | :--- |
| `capacity_orders` | Orders | Each order consumes exactly one capacity slot regardless of item count. |
| `inventory` values | Units of a SKU | Integer stock available at that warehouse for the whole batch. |
| `items` values | Units of a SKU | Positive integer demand; an order consumes these units from its assigned warehouse. |
| `shipping_costs` values | Currency | Finite, non-negative. Unit is dataset-defined (for example, nghìn đồng) but must be consistent within a dataset. |

Capacity and item quantity are deliberately different units: one order with ten
units still consumes one capacity slot.

---

## 6. Validation

Validation runs in two layers. JSON Schema cannot express cross-record rules, so
`scripts/validate_dataset.py` performs both layers.

### 6.1 Structural (JSON Schema Draft 2020-12)

- Valid JSON syntax and no duplicate object keys.
- All required fields present; no unknown fields at any level.
- Correct primitive types; booleans are not accepted as integers or numbers.
- `schema_version == "1.0"` and `policy == "A"`.
- `capacity_orders >= 0`, inventory stock `>= 0`, item quantity `>= 1`,
  shipping cost `>= 0` and finite.
- Non-empty arrays for `skus`, `warehouses`, and `orders`.

### 6.2 Semantic (executable Python)

- IDs are unique within `skus`, `warehouses`, and `orders`.
- Every warehouse declares every SKU in `inventory`; no unknown SKU keys.
- Every order item references a declared SKU.
- Every `shipping_costs` key references a declared warehouse.
- Shipping costs are finite (rejects `NaN` and `±Infinity`) and non-negative.
- Policy B fields (`penalty`, `split_penalty`, `unassigned_penalty`,
  `handling_cost_per_unit`, `daily_capacity`, `location_code`,
  `destination_zone`) are rejected.

Run the validator:

```bash
python scripts/validate_dataset.py data/samples/
```

### 6.3 Validity is not feasibility

- `VALID`: the dataset satisfies the contract above.
- `FEASIBLE`: at least one complete Policy A allocation exists.
- `INFEASIBLE`: exhaustive checking or a proven necessary condition shows that
  no complete allocation exists.
- `UNKNOWN`: the feasibility search stopped before proving either outcome.

An infeasible dataset is **not** structurally invalid. Never relabel it as such.

---

## 7. Feasibility oracle

`scripts/check_feasibility.py` performs deterministic backtracking for small
instances. It reports `FEASIBLE`, `INFEASIBLE`, `UNKNOWN`, or `INVALID`, plus an
example assignment and explored-state count when feasible.

```bash
python scripts/check_feasibility.py data/samples/sample_small.json
python scripts/check_feasibility.py data/samples/sample_small.json --json
```

The oracle is a verification tool for small fixtures. It does not replace the
optimization work owned by TV3 on medium and large instances.

---

## 8. Schema versioning

- `schema_version` is a literal string. Any change to required fields, types, or
  semantics requires a new version value and a new schema file revision.
- Within version `"1.0"`, additive metadata under `metadata` is allowed; all
  other object levels reject unknown fields.
- Dataset files must be updated, revalidated, and rechecked for feasibility when
  the version changes. Never silently reinterpret an old file.

---

## 9. Adding a dataset

1. Prefer the generator for feasible benchmarks:

   ```bash
   python scripts/generate_dataset.py \
     --warehouses 4 --orders 20 --skus 5 --seed 20261111 \
     --output data/samples/generated.json
   ```

2. For hand-built or edge cases, copy the structure in §2 and keep inventory
   complete for every warehouse.
3. Record provenance in `metadata` (`generator`, `seed`, or `note`).
4. Validate: `python scripts/validate_dataset.py <file>`.
5. Check feasibility: `python scripts/check_feasibility.py <file> --json`.
6. If infeasible, document the proving reason in `description` and confirm the
   file is still structurally valid.
7. Add the file to the catalogue in [`data/README.md`](../data/README.md) and to
   the expected-status table in `tests/test_datasets.py`.
8. Do not commit generated scratch output unless it becomes a reviewed fixture.

---

## 10. Legacy artifacts

| Artifact | Status | Notes |
| :--- | :--- | :--- |
| `benchmark_data.json` | Legacy | Input for the standalone `validate_orders.py` prototype. It uses a different flat schema (`capacity`, `current_occupancy`, `items[]`, Euclidean costs) and is intentionally **not** migrated. Do not treat it as a Policy A dataset. |
| Root `data-dictionary.md` | Deprecated | Replaced by this document; retained as a pointer only. |
| `docs/mathematical-model.md` §3 | Historical | Policy B formulation retained for reference; Policy A is canonical (§4 and ADR-004). |

TV3, TV5, and TV6 should consume files that validate against this contract, not
the legacy prototype input.
