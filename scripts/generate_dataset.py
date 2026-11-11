#!/usr/bin/env python3
"""Deterministic dataset generator for LogiMind Policy A benchmark datasets.

Generates reproducible datasets guaranteed to be feasible by construction.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

# Import local validator
try:
    from scripts.validate_dataset import validate_dataset_data, validate_file
except ImportError:
    # If run directly from scripts/ directory
    from validate_dataset import validate_dataset_data, validate_file


def generate_dataset(
    num_warehouses: int,
    num_orders: int,
    num_skus: int,
    seed: int,
    dataset_id: str | None = None,
    name: str | None = None,
    description: str | None = None,
) -> dict:
    """Generate a Policy A dataset guaranteed to be feasible by construction.

    Args:
        num_warehouses: Number of warehouses (must be >= 1).
        num_orders: Number of orders (must be >= 1).
        num_skus: Number of SKUs (must be >= 1).
        seed: Random seed for deterministic generation.
        dataset_id: Optional dataset identifier.
        name: Optional human-readable name.
        description: Optional description.

    Returns:
        Canonical Policy A dataset dictionary.
    """
    if num_warehouses < 1:
        raise ValueError(f"num_warehouses must be >= 1, got {num_warehouses}")
    if num_orders < 1:
        raise ValueError(f"num_orders must be >= 1, got {num_orders}")
    if num_skus < 1:
        raise ValueError(f"num_skus must be >= 1, got {num_skus}")

    rng = random.Random(seed)

    ds_id = dataset_id or f"generated-w{num_warehouses}-o{num_orders}-s{num_skus}-seed{seed}"
    ds_name = name or f"Generated Policy A Benchmark ({num_warehouses} WH, {num_orders} Orders, {num_skus} SKUs)"
    ds_desc = (
        description
        or f"Reproducible Policy A benchmark generated with seed {seed}. Feasible by construction."
    )

    # 1. Generate SKU catalogue
    skus: List[Dict[str, str]] = []
    sku_ids: List[str] = []
    for i in range(1, num_skus + 1):
        sid = f"SKU-{i:02d}"
        sku_ids.append(sid)
        skus.append({
            "sku_id": sid,
            "name": f"Product {sid}"
        })

    # 2. Generate Warehouses skeleton
    warehouse_ids: List[str] = [f"WH-{i:02d}" for i in range(1, num_warehouses + 1)]
    assigned_order_counts: Dict[str, int] = {wid: 0 for wid in warehouse_ids}
    warehouse_required_stock: Dict[str, Dict[str, int]] = {
        wid: {sid: 0 for sid in sku_ids} for wid in warehouse_ids
    }

    # 3. Generate Orders & construction assignment
    orders: List[Dict[str, Any]] = []
    for order_idx in range(1, num_orders + 1):
        oid = f"ORD-{order_idx:03d}"

        # Assign order to one warehouse to guarantee feasibility
        assigned_wh = warehouse_ids[(order_idx - 1) % num_warehouses]
        assigned_order_counts[assigned_wh] += 1

        # Pick 1 to min(3, num_skus) SKUs for this order
        num_items_in_order = rng.randint(1, min(3, num_skus))
        order_skus = rng.sample(sku_ids, num_items_in_order)
        order_items: Dict[str, int] = {}

        for sid in order_skus:
            qty = rng.randint(1, 5)
            order_items[sid] = qty
            warehouse_required_stock[assigned_wh][sid] += qty

        # Generate shipping costs
        # The assigned warehouse MUST have an available route
        shipping_costs: Dict[str, float] = {}
        # Cost to assigned warehouse (reasonable baseline)
        assigned_cost = round(rng.uniform(2.0, 15.0), 2)
        shipping_costs[assigned_wh] = assigned_cost

        # Routes to other warehouses may exist or be omitted
        for wid in warehouse_ids:
            if wid == assigned_wh:
                continue
            # 85% chance route is available
            if rng.random() < 0.85:
                # Cost can be higher, lower, or equal
                cost = round(rng.uniform(3.0, 35.0), 2)
                shipping_costs[wid] = cost

        orders.append({
            "order_id": oid,
            "items": order_items,
            "shipping_costs": shipping_costs
        })

    # 4. Finalize Warehouses with capacity and inventory (guaranteed sufficient)
    warehouses: List[Dict[str, Any]] = []
    for wid in warehouse_ids:
        # Capacity must be at least the number of assigned orders
        # Add a small buffer to avoid triviality while keeping realistic constraints
        cap_buffer = rng.randint(0, max(1, num_orders // (num_warehouses * 2)))
        capacity_orders = assigned_order_counts[wid] + cap_buffer

        # Inventory must be at least required stock, plus buffer
        inventory: Dict[str, int] = {}
        for sid in sku_ids:
            req = warehouse_required_stock[wid][sid]
            stock_buffer = rng.randint(0, 10)
            inventory[sid] = req + stock_buffer

        warehouses.append({
            "warehouse_id": wid,
            "name": f"Warehouse {wid}",
            "capacity_orders": capacity_orders,
            "inventory": inventory
        })

    dataset: Dict[str, Any] = {
        "schema_version": "1.0",
        "dataset_id": ds_id,
        "name": ds_name,
        "description": ds_desc,
        "policy": "A",
        "metadata": {
            "generator": "LogiMind TV2 dataset generator",
            "seed": seed
        },
        "skus": skus,
        "warehouses": warehouses,
        "orders": orders
    }

    return dataset


def main() -> int:
    """CLI entry point for generate_dataset.py."""
    parser = argparse.ArgumentParser(
        description="Generate deterministic LogiMind Policy A benchmark datasets."
    )
    parser.add_argument(
        "--warehouses",
        type=int,
        required=True,
        help="Number of warehouses to generate (integer >= 1).",
    )
    parser.add_argument(
        "--orders",
        type=int,
        required=True,
        help="Number of orders to generate (integer >= 1).",
    )
    parser.add_argument(
        "--skus",
        type=int,
        required=True,
        help="Number of SKUs to generate (integer >= 1).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        required=True,
        help="Random seed integer for deterministic reproducibility.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output JSON file path.",
    )
    parser.add_argument(
        "--dataset-id",
        type=str,
        default=None,
        help="Optional custom dataset_id.",
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Optional human-readable dataset name.",
    )
    parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="Optional dataset description.",
    )

    args = parser.parse_args()

    try:
        dataset = generate_dataset(
            num_warehouses=args.warehouses,
            num_orders=args.orders,
            num_skus=args.skus,
            seed=args.seed,
            dataset_id=args.dataset_id,
            name=args.name,
            description=args.description,
        )
    except ValueError as exc:
        print(f"[ERROR] Invalid generation arguments: {exc}", file=sys.stderr)
        return 1

    # Validate generated data in-memory before writing
    is_valid, errors = validate_dataset_data(dataset)
    if not is_valid:
        print("[FATAL] Generated dataset failed schema/semantic validation:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    output_path = Path(args.output)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
            f.write("\n")
    except OSError as exc:
        print(f"[ERROR] Failed to write output file '{output_path}': {exc}", file=sys.stderr)
        return 1

    # Re-read and validate the file exactly as written, so the command only
    # reports success when the on-disk artifact satisfies the canonical schema.
    is_valid, errors = validate_file(output_path)
    if not is_valid:
        print("[FATAL] Written dataset failed validation:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"[SUCCESS] Generated feasible dataset -> {output_path}")
    print(f"  Warehouses: {args.warehouses}")
    print(f"  Orders:     {args.orders}")
    print(f"  SKUs:       {args.skus}")
    print(f"  Seed:       {args.seed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
