#!/usr/bin/env python3
"""Dataset validation script for LogiMind Policy A benchmark datasets.

Validates:
1. JSON syntax, file readability, and duplicate JSON object keys.
2. JSON Schema Draft 2020-12 conformance against ``data/schema/dataset.schema.json``.
3. Strict cross-record integrity that JSON Schema alone cannot express:
   - Unique SKU, warehouse, and order IDs.
   - Complete inventory mappings (every warehouse declares every known SKU).
   - Valid SKU references in order items.
   - Valid warehouse references in shipping costs.
   - Rejection of boolean values in integer/numeric fields.
   - Finite, non-negative shipping costs and positive integer order quantities.
   - Policy A conformance (rejection of Policy B fields).

This module is imported by ``generate_dataset.py`` and ``check_feasibility.py``;
the command-line interface is documented in ``scripts/README.md``.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

try:
    import jsonschema
except ImportError:  # pragma: no cover - exercised only in a broken environment
    jsonschema = None  # type: ignore[assignment]

DEFAULT_SCHEMA_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "schema" / "dataset.schema.json"
)

# Fields that belong to Policy B. They are never part of the Policy A contract.
FORBIDDEN_POLICY_B_FIELDS = {
    "split_penalty",
    "unassigned_penalty",
    "handling_cost_per_unit",
    "daily_capacity",
    "location_code",
    "destination_zone",
    "penalty",
}

MISSING_JSONSCHEMA_MESSAGE = (
    "The 'jsonschema' package is required for dataset validation. "
    "Install it with: pip install jsonschema"
)


class DuplicateKeyError(ValueError):
    """Raised when a JSON object contains the same key more than once."""


def _object_pairs_without_duplicates(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    """Build a dict from JSON pairs, rejecting duplicate object keys."""
    result: Dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"Duplicate object key: '{key}'")
        result[key] = value
    return result


def load_json_schema(schema_path: Path) -> dict:
    """Load and parse the JSON Schema file."""
    if not schema_path.is_file():
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _require_jsonschema() -> None:
    """Fail loudly when the schema engine is unavailable."""
    if jsonschema is None:
        raise RuntimeError(MISSING_JSONSCHEMA_MESSAGE)


def _as_list(value: Any) -> List[Any]:
    """Return ``value`` when it is a list, else an empty list."""
    return value if isinstance(value, list) else []


def _as_dict(value: Any) -> Dict[str, Any]:
    """Return ``value`` when it is a dict, else an empty dict."""
    return value if isinstance(value, dict) else {}


def _check_no_booleans(data: Any, path: str = "") -> List[str]:
    """Ensure no boolean value is used in a numeric or integer field.

    JSON Schema type checks already exclude booleans for ``integer``/``number``
    under Draft 2020-12, but this explicit walk produces clearer field-level
    messages and protects the contract if the schema is ever relaxed.
    """
    errors: List[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            if key in {"capacity_orders", "seed"} and isinstance(value, bool):
                errors.append(f"Field '{current_path}' must be an integer, got boolean.")
            elif key == "inventory" and isinstance(value, dict):
                for sku, stock in value.items():
                    if isinstance(stock, bool):
                        errors.append(
                            f"Inventory '{current_path}.{sku}' must be an integer, got boolean."
                        )
            elif key == "items" and isinstance(value, dict):
                for sku, qty in value.items():
                    if isinstance(qty, bool):
                        errors.append(
                            f"Order item '{current_path}.{sku}' must be an integer, got boolean."
                        )
            elif key == "shipping_costs" and isinstance(value, dict):
                for warehouse, cost in value.items():
                    if isinstance(cost, bool):
                        errors.append(
                            f"Shipping cost '{current_path}.{warehouse}' must be a number, "
                            "got boolean."
                        )
            else:
                errors.extend(_check_no_booleans(value, current_path))
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            errors.extend(_check_no_booleans(item, f"{path}[{idx}]"))
    return errors


def validate_dataset_data(data: Any, schema: dict | None = None) -> Tuple[bool, List[str]]:
    """Validate a parsed dataset against the schema and Policy A semantic rules.

    Args:
        data: Parsed JSON object.
        schema: Optional parsed JSON Schema dict. When omitted, the canonical
            schema at ``data/schema/dataset.schema.json`` is loaded.

    Returns:
        Tuple of ``(is_valid, errors)``. ``errors`` is empty only when the
        dataset satisfies both the structural schema and the semantic rules.
    """
    _require_jsonschema()
    errors: List[str] = []

    if not isinstance(data, dict):
        return False, ["Dataset root must be a JSON object."]

    # 1. Structural JSON Schema validation.
    if schema is None:
        schema = load_json_schema(DEFAULT_SCHEMA_PATH)

    validator = jsonschema.Draft202012Validator(schema)
    schema_errors = sorted(validator.iter_errors(data), key=lambda e: [str(p) for p in e.path])
    for err in schema_errors:
        loc = ".".join(str(p) for p in err.path) or "root"
        errors.append(f"Schema violation at '{loc}': {err.message}")

    # 2. Explicit boolean rejection with field-level messages.
    errors.extend(_check_no_booleans(data))

    if any(e.startswith("Schema violation at 'root'") for e in errors):
        return False, errors

    # 3. Policy B fields must never appear in a Policy A dataset.
    for forbidden in FORBIDDEN_POLICY_B_FIELDS:
        if forbidden in data:
            errors.append(f"Forbidden Policy B field found in dataset root: '{forbidden}'")
        parameters = data.get("parameters")
        if isinstance(parameters, dict) and forbidden in parameters:
            errors.append(f"Forbidden Policy B parameter found: '{forbidden}'")

    warehouses = _as_list(data.get("warehouses"))
    orders = _as_list(data.get("orders"))
    skus = _as_list(data.get("skus"))

    for idx, warehouse in enumerate(warehouses):
        if not isinstance(warehouse, dict):
            continue
        for forbidden in FORBIDDEN_POLICY_B_FIELDS:
            if forbidden in warehouse:
                errors.append(
                    f"Warehouse '{warehouse.get('warehouse_id', idx)}' contains "
                    f"forbidden Policy B field '{forbidden}'"
                )

    for idx, order in enumerate(orders):
        if not isinstance(order, dict):
            continue
        for forbidden in FORBIDDEN_POLICY_B_FIELDS:
            if forbidden in order:
                errors.append(
                    f"Order '{order.get('order_id', idx)}' contains "
                    f"forbidden Policy B field '{forbidden}'"
                )

    # 4. Unique identifiers.
    sku_ids: Set[str] = set()
    for idx, sku in enumerate(skus):
        if not isinstance(sku, dict):
            continue
        sku_id = sku.get("sku_id")
        if isinstance(sku_id, str):
            if sku_id in sku_ids:
                errors.append(f"Duplicate sku_id: '{sku_id}' at skus[{idx}]")
            sku_ids.add(sku_id)

    warehouse_ids: Set[str] = set()
    for idx, warehouse in enumerate(warehouses):
        if not isinstance(warehouse, dict):
            continue
        warehouse_id = warehouse.get("warehouse_id")
        if isinstance(warehouse_id, str):
            if warehouse_id in warehouse_ids:
                errors.append(f"Duplicate warehouse_id: '{warehouse_id}' at warehouses[{idx}]")
            warehouse_ids.add(warehouse_id)

    order_ids: Set[str] = set()
    for idx, order in enumerate(orders):
        if not isinstance(order, dict):
            continue
        order_id = order.get("order_id")
        if isinstance(order_id, str):
            if order_id in order_ids:
                errors.append(f"Duplicate order_id: '{order_id}' at orders[{idx}]")
            order_ids.add(order_id)

    # 5. Every warehouse must declare inventory for every known SKU exactly once.
    for warehouse in warehouses:
        if not isinstance(warehouse, dict):
            continue
        warehouse_id = warehouse.get("warehouse_id", "<unknown>")
        inventory = warehouse.get("inventory")
        if not isinstance(inventory, dict):
            continue

        missing_skus = sku_ids - set(inventory.keys())
        if missing_skus:
            errors.append(
                f"Warehouse '{warehouse_id}' is missing inventory mapping for declared SKUs: "
                f"{sorted(missing_skus)}"
            )
        extra_skus = set(inventory.keys()) - sku_ids
        if extra_skus:
            errors.append(
                f"Warehouse '{warehouse_id}' contains inventory for unknown SKUs: "
                f"{sorted(extra_skus)}"
            )

    # 6. Order item references, quantities, and shipping-cost routes.
    for order in orders:
        if not isinstance(order, dict):
            continue
        order_id = order.get("order_id", "<unknown>")
        items = order.get("items")
        if isinstance(items, dict):
            if not items:
                errors.append(f"Order '{order_id}' items dictionary must not be empty.")
            for sku, qty in items.items():
                if sku not in sku_ids:
                    errors.append(f"Order '{order_id}' references undeclared SKU: '{sku}'")
                if isinstance(qty, bool):
                    continue
                if isinstance(qty, int):
                    if qty <= 0:
                        errors.append(
                            f"Order '{order_id}' item '{sku}' has non-positive "
                            f"quantity: {qty}"
                        )

        shipping_costs = order.get("shipping_costs")
        if isinstance(shipping_costs, dict):
            for warehouse_id, cost in shipping_costs.items():
                if warehouse_id not in warehouse_ids:
                    errors.append(
                        f"Order '{order_id}' shipping cost references undeclared "
                        f"warehouse: '{warehouse_id}'"
                    )
                if isinstance(cost, bool):
                    continue
                if isinstance(cost, (int, float)):
                    if not math.isfinite(cost):
                        errors.append(
                            f"Order '{order_id}' shipping cost to warehouse "
                            f"'{warehouse_id}' is non-finite: {cost}"
                        )
                    elif cost < 0:
                        errors.append(
                            f"Order '{order_id}' shipping cost to warehouse "
                            f"'{warehouse_id}' is negative: {cost}"
                        )

    return len(errors) == 0, errors


def validate_file(file_path: Path, schema: dict | None = None) -> Tuple[bool, List[str]]:
    """Validate a single dataset JSON file.

    Returns:
        Tuple of ``(is_valid, errors)``.
    """
    if not file_path.is_file():
        return False, [f"File not found: {file_path}"]

    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, [f"Failed to read file: {exc}"]

    try:
        data = json.loads(content, object_pairs_hook=_object_pairs_without_duplicates)
    except DuplicateKeyError as exc:
        return False, [f"Invalid JSON object: {exc}"]
    except json.JSONDecodeError as exc:
        return False, [f"Invalid JSON syntax at line {exc.lineno}, col {exc.colno}: {exc.msg}"]

    return validate_dataset_data(data, schema)


def main() -> int:
    """CLI entry point for ``scripts/validate_dataset.py``."""
    parser = argparse.ArgumentParser(
        description="Validate LogiMind Policy A benchmark datasets against the canonical schema."
    )
    parser.add_argument(
        "target",
        type=str,
        help="Path to a JSON dataset file or a directory containing dataset files.",
    )
    parser.add_argument(
        "--schema",
        type=str,
        default=str(DEFAULT_SCHEMA_PATH),
        help=f"Path to the JSON Schema file (default: {DEFAULT_SCHEMA_PATH})",
    )
    args = parser.parse_args()

    if jsonschema is None:
        print(f"[FATAL] {MISSING_JSONSCHEMA_MESSAGE}", file=sys.stderr)
        return 1

    schema_path = Path(args.schema)
    try:
        schema = load_json_schema(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FATAL] Failed to load schema from '{schema_path}': {exc}", file=sys.stderr)
        return 1

    target_path = Path(args.target)
    if target_path.is_file():
        files_to_check = [target_path]
    elif target_path.is_dir():
        files_to_check = sorted(target_path.glob("*.json"))
        if not files_to_check:
            print(f"[WARNING] No .json files found in directory: {target_path}")
            return 0
    else:
        print(f"[FATAL] Target path does not exist: {target_path}", file=sys.stderr)
        return 1

    failed_count = 0
    for file_path in files_to_check:
        is_valid, errors = validate_file(file_path, schema)
        if is_valid:
            print(f"[PASS] {file_path.name}")
        else:
            print(f"[FAIL] {file_path.name}")
            for error in errors:
                print(f"  - ERROR: {error}")
            failed_count += 1

    print()
    print(f"{len(files_to_check)} datasets validated.")
    print(f"{failed_count} validation errors.")

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
