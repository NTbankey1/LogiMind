# Mathematical Model Specification: LogiMind

> **Document Status:** Draft Specification Template (Pending TV1 Validation & Faculty Review)  
> **Primary Owner:** TV1 (Business Analysis & Mathematical Modeling)  
> **Co-Owner / Implementation:** TV3 (Optimization Algorithms)

---

## 1. Overview & Modeling Philosophy

The primary purpose of this document is to establish the mathematical formulation for the Multi-Warehouse Order Allocation Problem (MWOAP) in the LogiMind project. 

- Sections labeled **[Confirmed]** represent agreed-upon team baselines.
- Sections labeled **[Pending TV1 Review]** or **[TBD]** contain proposed formulation templates to be validated, refined, or extended by TV1.

---

## 2. Sets and Indices

| Symbol | Description | Status |
| :--- | :--- | :--- |
| $O$ | Set of customer orders, indexed by $i \in O = \{1, \dots, |O|\}$ | [Confirmed] |
| $W$ | Set of warehouses / fulfillment centers, indexed by $j \in W = \{1, \dots, |W|\}$ | [Confirmed] |
| $K$ | Set of distinct product items (SKUs), indexed by $k \in K = \{1, \dots, |K|\}$ | [Confirmed] |
| $L_i$ | Set of order line items for order $i$ | [Pending TV1 Review] |

---

## 3. Input Parameters

| Parameter | Unit | Description | Status |
| :--- | :--- | :--- | :--- |
| $D_{i, k}$ | Units | Quantity of SKU $k$ demanded by order $i$ | [Confirmed] |
| $I_{j, k}$ | Units | Available inventory of SKU $k$ at warehouse $j$ | [Confirmed] |
| $C_j$ | Orders or Units | Maximum processing / throughput capacity of warehouse $j$ in the planning period | [Pending TV1 Review: Units vs. Orders] |
| $S_{i, j}$ | Currency ($) | Shipping cost to deliver order $i$ from warehouse $j$ to destination | [Confirmed] |
| $H_{j, k}$ | Currency ($) | Handling / picking cost per unit of SKU $k$ at warehouse $j$ | [Pending TV1 Review] |
| $P_{split}$ | Currency ($) | Penalty cost incurred when an order is split across more than one warehouse | [Pending TV1 Review] |
| $P_{unassigned}$ | Currency ($) | Penalty cost per unfulfilled order or unit if global capacity is exceeded | [Pending TV1 Review] |

---

## 4. Decision Variables

### Proposed Baseline Formulation [Pending TV1 Review]

1. **Continuous / Integer Allocation Variable:**
   $$x_{i, j, k} \ge 0 \quad (\text{or } x_{i, j, k} \in \mathbb{Z}^+)$$
   Quantity of SKU $k$ for order $i$ fulfilled from warehouse $j$.

2. **Binary Warehouse-to-Order Assignment:**
   $$y_{i, j} \in \{0, 1\}$$
   $y_{i, j} = 1$ if warehouse $j$ fulfills any portion of order $i$; $0$ otherwise.

3. **Binary Order Split Indicator:**
   $$z_i \in \{0, 1\}$$
   $z_i = 1$ if order $i$ is fulfilled by more than one warehouse (split shipment); $0$ otherwise.

4. **Slack / Unfulfilled Variable (for Feasibility):**
   $$u_{i, k} \ge 0$$
   Quantity of SKU $k$ in order $i$ left unfulfilled if global capacity/stock is exhausted.

---

## 5. Objective Function [Draft Proposal - Pending TV1 Review]

Minimize the total fulfillment cost, composed of shipping costs, handling costs, split-shipment penalties, and unfulfilled demand penalties:

$$\min Z = \sum_{i \in O} \sum_{j \in W} S_{i, j} \cdot y_{i, j} + \sum_{i \in O} \sum_{j \in W} \sum_{k \in K} H_{j, k} \cdot x_{i, j, k} + P_{split} \sum_{i \in O} z_i + P_{unassigned} \sum_{i \in O} \sum_{k \in K} u_{i, k}$$

*(Note: TV1 will verify whether shipping cost is flat per shipment $y_{i,j}$ or weight/volume dependent).*

---

## 6. Constraints [Draft Proposal - Pending TV1 Review]

1. **Demand Satisfaction:**
   For every order $i \in O$ and SKU $k \in K$:
   $$\sum_{j \in W} x_{i, j, k} + u_{i, k} = D_{i, k}$$

2. **Warehouse Inventory Availability:**
   For every warehouse $j \in W$ and SKU $k \in K$:
   $$\sum_{i \in O} x_{i, j, k} \le I_{j, k}$$

3. **Warehouse Processing Capacity:**
   For every warehouse $j \in W$:
   $$\sum_{i \in O} \sum_{k \in K} x_{i, j, k} \le C_j \quad (\text{or based on order count: } \sum_{i \in O} y_{i, j} \le C_j)$$

4. **Link Allocation to Binary Indicator ($y_{i, j}$):**
   For every order $i$, warehouse $j$, and SKU $k$:
   $$x_{i, j, k} \le D_{i, k} \cdot y_{i, j}$$

5. **Split Shipment Detection ($z_i$):**
   For every order $i \in O$:
   $$\sum_{j \in W} y_{i, j} - 1 \le M \cdot z_i \quad (\text{where } M = |W|)$$

6. **Variable Bounds & Integrality:**
   $$x_{i, j, k} \in \mathbb{Z}^+, \quad y_{i, j} \in \{0, 1\}, \quad z_i \in \{0, 1\}, \quad u_{i, k} \ge 0$$

---

## 7. Assumptions [Pending TV1 Review]

- [ ] Orders arriving in a planning batch are considered known and static.
- [ ] Lead times between warehouses are not considered in the daily allocation tier.
- [ ] Partial line-item splitting (splitting a single SKU within an order across 2 warehouses) is forbidden unless explicitly permitted.
- [ ] Stock quantities $I_{j, k}$ are reserved instantaneously upon solver solution confirmation.

---

## 8. Infeasible Cases & Unassigned-Order Policy

When total demand exceeds available inventory or warehouse throughput capacity:
1. **Hard Failure Mode:** The solver returns status `INFEASIBLE`.
2. **Elastic Slack Mode (Recommended):** The solver introduces slack variables $u_{i, k}$ with a heavy penalty $P_{unassigned} \gg \max(S_{i, j})$. This guarantees a solution is always found, prioritizing fulfillable orders while identifying the exact shortfall.

TV1 will formally specify the policy chosen for LogiMind.

---

## 9. Small Hand-Calculated Example (Toy Problem)

### Scenario Setup
- **Warehouses:** $W = \{W_1, W_2\}$
- **SKUs:** $K = \{A\}$
- **Inventory:**
  - $W_1$: 10 units of $A$
  - $W_2$: 10 units of $A$
- **Warehouse Daily Capacity:**
  - $C_1 = 8$ units
  - $C_2 = 8$ units
- **Customer Orders:**
  - Order 1: 6 units of $A$ (Customer near $W_1$)
    - Shipping cost: $S_{1, 1} = \$5$, $S_{1, 2} = \$12$
  - Order 2: 5 units of $A$ (Customer near $W_1$)
    - Shipping cost: $S_{2, 1} = \$6$, $S_{2, 2} = \$11$

### Baseline Heuristic (Greedy Nearest First)
1. Order 1 arrives: assigned to nearest warehouse $W_1$ (cost = \$5). Remaining capacity at $W_1 = 8 - 6 = 2$.
2. Order 2 arrives: needs 5 units. $W_1$ only has 2 capacity left! Order 2 must be routed entirely to $W_2$ (cost = \$11).
3. **Total Cost (Baseline) = \$5 + \$11 = \$16.**

### Optimal MILP Allocation
1. If Order 2 is assigned to $W_1$ (cost = \$6), capacity at $W_1$ becomes $8 - 5 = 3$.
2. Order 1 needs 6 units $\to$ exceeds remaining $W_1$ capacity $\to$ routed to $W_2$ (cost = \$12). Total = \$18.
3. Therefore, greedy was optimal in this tiny instance (\$16).
4. *Now suppose Order 1 shipping to $W_2$ was \$7 instead of \$12:*
   - Greedy: Order 1 $\to W_1$ (\$5) + Order 2 $\to W_2$ (\$11) = **\$16**.
   - Optimal: Order 2 $\to W_1$ (\$6) + Order 1 $\to W_2$ (\$7) = **\$13** (Optimization gain: \$3 savings).

This illustrates how global optimization resolves local bottleneck conflicts.
