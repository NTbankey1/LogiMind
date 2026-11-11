#!/usr/bin/env python3
"""Exhaustive small-instance feasibility checker for LogiMind Policy A datasets.

Verifies whether a valid Policy A dataset admits at least one complete allocation
satisfying:
1. Exactly one warehouse per order.
2. Route availability (warehouse exists in order.shipping_costs).
3. Per-SKU inventory non-exceedance at each warehouse.
4. Total order processing capacity non-exceedance at each warehouse.

Returns statuses:
- FEASIBLE: complete valid allocation found.
- INFEASIBLE: search space exhausted without solution (proven impossible).
- UNKNOWN: state search limit reached without conclusive proof.
- INVALID: dataset fails schema or semantic validation.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from scripts.validate_dataset import validate_dataset_data
except ImportError:
    from validate_dataset import validate_dataset_data


class FeasibilityStatus(str, Enum):
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"


@dataclass
class FeasibilityResult:
    status: FeasibilityStatus
    states_explored: int
    assignment: Optional[Dict[str, str]] = None
    total_shipping_cost: Optional[float] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "status": self.status.value,
            "states_explored": self.states_explored,
        }
        if self.assignment is not None:
            result["assignment"] = self.assignment
        if self.total_shipping_cost is not None:
            result["total_shipping_cost"] = round(self.total_shipping_cost, 2)
        if self.message:
            result["message"] = self.message
        return result


def check_dataset_feasibility(
    data: Dict[str, Any],
    max_states: int = 500_000,
) -> FeasibilityResult:
    """Run deterministic exhaustive search on a Policy A dataset.

    Args:
        data: Parsed dataset dictionary.
        max_states: Search state threshold before returning UNKNOWN.

    Returns:
        FeasibilityResult with status and execution details.
    """
    # 1. Structural and semantic validation
    is_valid, validation_errors = validate_dataset_data(data)
    if not is_valid:
        return FeasibilityResult(
            status=FeasibilityStatus.INVALID,
            states_explored=0,
            message="; ".join(validation_errors),
        )

    # 2. Extract immutable structures
    warehouses_data = data["warehouses"]
    orders_data = data["orders"]

    # Quick necessary condition: total warehouse capacity >= total orders
    total_capacity = sum(wh["capacity_orders"] for wh in warehouses_data)
    total_orders = len(orders_data)
    if total_capacity < total_orders:
        return FeasibilityResult(
            status=FeasibilityStatus.INFEASIBLE,
            states_explored=1,
            message=f"Total warehouse capacity ({total_capacity}) < total orders ({total_orders}).",
        )

    # Quick necessary condition: for each SKU, total warehouse stock >= total SKU demand
    sku_total_demand: Dict[str, int] = {}
    for ord_item in orders_data:
        for sku, qty in ord_item["items"].items():
            sku_total_demand[sku] = sku_total_demand.get(sku, 0) + qty

    sku_total_stock: Dict[str, int] = {}
    for wh in warehouses_data:
        for sku, stock in wh["inventory"].items():
            sku_total_stock[sku] = sku_total_stock.get(sku, 0) + stock

    for sku, dem in sku_total_demand.items():
        if dem > sku_total_stock.get(sku, 0):
            return FeasibilityResult(
                status=FeasibilityStatus.INFEASIBLE,
                states_explored=1,
                message=f"Total stock for SKU '{sku}' ({sku_total_stock.get(sku, 0)}) < total demand ({dem}).",
            )

    # Quick necessary condition: each individual order must be fulfillable by at least one warehouse
    for ord_item in orders_data:
        oid = ord_item["order_id"]
        shipping_costs = ord_item.get("shipping_costs", {})
        fulfillable_wh_count = 0
        for wh in warehouses_data:
            wid = wh["warehouse_id"]
            if wid not in shipping_costs:
                continue
            if wh["capacity_orders"] < 1:
                continue
            has_stock = True
            for sku, qty in ord_item["items"].items():
                if wh["inventory"].get(sku, 0) < qty:
                    has_stock = False
                    break
            if has_stock:
                fulfillable_wh_count += 1
        if fulfillable_wh_count == 0:
            return FeasibilityResult(
                status=FeasibilityStatus.INFEASIBLE,
                states_explored=1,
                message=f"Order '{oid}' cannot be fulfilled by any warehouse due to missing route, zero capacity, or stock.",
            )

    # 3. Setup exhaustive search state
    # Work with copies of capacity and inventory to avoid mutating input
    remaining_capacity: Dict[str, int] = {
        wh["warehouse_id"]: wh["capacity_orders"] for wh in warehouses_data
    }
    remaining_inventory: Dict[str, Dict[str, int]] = {
        wh["warehouse_id"]: dict(wh["inventory"]) for wh in warehouses_data
    }

    # Deterministic order list
    # Sort orders by candidate warehouse count (MRV heuristic: most constrained first)
    order_candidates: List[Tuple[int, str, Dict[str, Any]]] = []
    for ord_item in orders_data:
        oid = ord_item["order_id"]
        routes = ord_item.get("shipping_costs", {})
        cand_count = sum(1 for wid in remaining_capacity if wid in routes)
        order_candidates.append((cand_count, oid, ord_item))

    # Tie break on order_id
    order_candidates.sort(key=lambda t: (t[0], t[1]))
    sorted_orders = [t[2] for t in order_candidates]

    state_counter = 0
    hit_limit = False
    current_assignment: Dict[str, str] = {}
    found_solution: Optional[Dict[str, str]] = None
    found_cost: Optional[float] = None

    def backtrack(order_idx: int) -> bool:
        nonlocal state_counter, hit_limit, found_solution, found_cost
        state_counter += 1
        if state_counter > max_states:
            hit_limit = True
            return False

        if order_idx == len(sorted_orders):
            # All orders assigned!
            found_solution = dict(current_assignment)
            # Calculate total cost
            tot_cost = 0.0
            for o in sorted_orders:
                oid = o["order_id"]
                assigned_wh = found_solution[oid]
                tot_cost += o["shipping_costs"][assigned_wh]
            found_cost = tot_cost
            return True

        order = sorted_orders[order_idx]
        oid = order["order_id"]
        shipping_costs = order.get("shipping_costs", {})
        items = order["items"]

        # Deterministic warehouse iteration: sort warehouse IDs alphabetically
        for wid in sorted(remaining_capacity.keys()):
            # 1. Route must exist
            if wid not in shipping_costs:
                continue

            # 2. Capacity must be available
            if remaining_capacity[wid] <= 0:
                continue

            # 3. Stock must be sufficient for all items
            inv = remaining_inventory[wid]
            can_fulfill = True
            for sku, req_qty in items.items():
                if inv.get(sku, 0) < req_qty:
                    can_fulfill = False
                    break
            if not can_fulfill:
                continue

            # Forward step: deduct capacity and stock
            remaining_capacity[wid] -= 1
            for sku, req_qty in items.items():
                inv[sku] -= req_qty
            current_assignment[oid] = wid

            # Recurse
            if backtrack(order_idx + 1):
                return True

            # Backward step: backtrack
            remaining_capacity[wid] += 1
            for sku, req_qty in items.items():
                inv[sku] += req_qty
            del current_assignment[oid]

            if hit_limit:
                return False

        return False

    backtrack(0)

    if found_solution is not None:
        return FeasibilityResult(
            status=FeasibilityStatus.FEASIBLE,
            states_explored=state_counter,
            assignment=found_solution,
            total_shipping_cost=found_cost,
        )
    elif hit_limit:
        return FeasibilityResult(
            status=FeasibilityStatus.UNKNOWN,
            states_explored=state_counter,
            message=f"Reached search-state limit ({max_states}) without finding a solution.",
        )
    else:
        return FeasibilityResult(
            status=FeasibilityStatus.INFEASIBLE,
            states_explored=state_counter,
            message="Search space exhausted; no valid complete allocation exists.",
        )


def check_file(file_path: Path, max_states: int = 500_000) -> FeasibilityResult:
    """Check feasibility of a dataset file."""
    if not file_path.is_file():
        return FeasibilityResult(
            status=FeasibilityStatus.INVALID,
            states_explored=0,
            message=f"File not found: {file_path}",
        )

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:
        return FeasibilityResult(
            status=FeasibilityStatus.INVALID,
            states_explored=0,
            message=f"JSON parse error: {exc}",
        )

    return check_dataset_feasibility(data, max_states=max_states)


def main() -> int:
    """CLI entry point for check_feasibility.py."""
    parser = argparse.ArgumentParser(
        description="Check feasibility of LogiMind Policy A benchmark dataset via deterministic search."
    )
    parser.add_argument(
        "target",
        type=str,
        help="Path to dataset JSON file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result in machine-readable JSON format.",
    )
    parser.add_argument(
        "--max-states",
        type=int,
        default=500_000,
        help="Maximum search states explored before returning UNKNOWN (default: 500,000).",
    )
    args = parser.parse_args()

    file_path = Path(args.target)
    result = check_file(file_path, max_states=args.max_states)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"File:            {file_path.name}")
        print(f"Status:          {result.status.value}")
        print(f"States explored: {result.states_explored}")
        if result.message:
            print(f"Details:         {result.message}")
        if result.status == FeasibilityStatus.FEASIBLE and result.assignment:
            print("Allocation:")
            for oid in sorted(result.assignment.keys()):
                wid = result.assignment[oid]
                print(f"  {oid} -> {wid}")
            if result.total_shipping_cost is not None:
                print(f"Total Shipping Cost: {result.total_shipping_cost:.2f}")

    if result.status == FeasibilityStatus.FEASIBLE:
        return 0
    elif result.status == FeasibilityStatus.INFEASIBLE:
        return 0  # Feasibility check itself succeeded in proving infeasibility
    elif result.status == FeasibilityStatus.UNKNOWN:
        return 2
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
