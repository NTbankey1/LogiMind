"""Automated test suite for LogiMind TV2 Policy A datasets, generator, and validator."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_dataset import (
    load_json_schema,
    validate_dataset_data,
    validate_file,
)
from scripts.generate_dataset import generate_dataset
from scripts.check_feasibility import (
    FeasibilityStatus,
    check_dataset_feasibility,
    check_file,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = REPO_ROOT / "data" / "samples"
SCHEMA_PATH = REPO_ROOT / "data" / "schema" / "dataset.schema.json"


class TestDatasetSchemaAndValidation(unittest.TestCase):
    """Tests for dataset schema validation and semantic integrity rules."""

    @classmethod
    def setUpClass(cls):
        cls.schema = load_json_schema(SCHEMA_PATH)
        with open(SAMPLES_DIR / "sample_small.json", "r", encoding="utf-8") as f:
            cls.small_valid_data = json.load(f)

    def test_sample_small_passes_validation(self):
        is_valid, errors = validate_file(SAMPLES_DIR / "sample_small.json", self.schema)
        self.assertTrue(is_valid, f"sample_small.json failed validation: {errors}")

    def test_sample_medium_passes_validation(self):
        is_valid, errors = validate_file(SAMPLES_DIR / "sample_medium.json", self.schema)
        self.assertTrue(is_valid, f"sample_medium.json failed validation: {errors}")

    def test_sample_large_passes_validation(self):
        is_valid, errors = validate_file(SAMPLES_DIR / "sample_large.json", self.schema)
        self.assertTrue(is_valid, f"sample_large.json failed validation: {errors}")

    def test_infeasible_fixtures_pass_structural_validation(self):
        """Infeasible datasets must be structurally valid JSON conforming to schema."""
        for fixture in ["sample_infeasible.json", "edge_infeasible_stock.json"]:
            path = SAMPLES_DIR / fixture
            is_valid, errors = validate_file(path, self.schema)
            self.assertTrue(is_valid, f"{fixture} should be structurally valid: {errors}")

    def test_missing_required_top_level_field_fails(self):
        required_fields = [
            "schema_version",
            "dataset_id",
            "name",
            "description",
            "policy",
            "skus",
            "warehouses",
            "orders",
        ]
        for req in required_fields:
            corrupt = copy.deepcopy(self.small_valid_data)
            del corrupt[req]
            is_valid, errors = validate_dataset_data(corrupt, self.schema)
            self.assertFalse(is_valid, f"Missing '{req}' should fail")

    def test_unknown_top_level_field_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["unexpected_custom_field"] = "bad"
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("unexpected_custom_field" in e for e in errors))

    def test_policy_b_fields_rejected(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["parameters"] = {"split_penalty": 10.0}
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)

        corrupt2 = copy.deepcopy(self.small_valid_data)
        corrupt2["warehouses"][0]["daily_capacity"] = 10
        is_valid2, errors2 = validate_dataset_data(corrupt2, self.schema)
        self.assertFalse(is_valid2)

    def test_policy_b_rejected_by_policy_field(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["policy"] = "B"
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)

    def test_duplicate_sku_ids_fail(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["skus"].append({"sku_id": "SKU-A", "name": "Duplicate SKU"})
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("Duplicate sku_id" in e for e in errors))

    def test_duplicate_warehouse_ids_fail(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        dup_wh = copy.deepcopy(corrupt["warehouses"][0])
        corrupt["warehouses"].append(dup_wh)
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("Duplicate warehouse_id" in e for e in errors))

    def test_duplicate_order_ids_fail(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        dup_ord = copy.deepcopy(corrupt["orders"][0])
        corrupt["orders"].append(dup_ord)
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("Duplicate order_id" in e for e in errors))

    def test_unknown_sku_reference_in_order_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["orders"][0]["items"]["SKU-NONEXISTENT"] = 2
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("undeclared SKU" in e for e in errors))

    def test_unknown_warehouse_reference_in_shipping_costs_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["orders"][0]["shipping_costs"]["WH-NONEXISTENT"] = 12.5
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("undeclared warehouse" in e for e in errors))

    def test_missing_inventory_sku_mapping_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        del corrupt["warehouses"][0]["inventory"]["SKU-B"]
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("missing inventory mapping" in e for e in errors))

    def test_negative_stock_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["warehouses"][0]["inventory"]["SKU-A"] = -5
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)

    def test_negative_capacity_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["warehouses"][0]["capacity_orders"] = -1
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)

    def test_negative_shipping_cost_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["orders"][0]["shipping_costs"]["WH-01"] = -4.0
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)

    def test_boolean_values_rejected_for_integers_and_numbers(self):
        # Boolean as quantity
        corrupt1 = copy.deepcopy(self.small_valid_data)
        corrupt1["orders"][0]["items"]["SKU-A"] = True
        is_valid1, errors1 = validate_dataset_data(corrupt1, self.schema)
        self.assertFalse(is_valid1)
        self.assertTrue(any("boolean" in e.lower() or "not of type" in e.lower() for e in errors1))

        # Boolean as capacity
        corrupt2 = copy.deepcopy(self.small_valid_data)
        corrupt2["warehouses"][0]["capacity_orders"] = True
        is_valid2, errors2 = validate_dataset_data(corrupt2, self.schema)
        self.assertFalse(is_valid2)
        self.assertTrue(any("boolean" in e.lower() or "not of type" in e.lower() for e in errors2))

        # Boolean as shipping cost
        corrupt3 = copy.deepcopy(self.small_valid_data)
        corrupt3["orders"][0]["shipping_costs"]["WH-01"] = True
        is_valid3, errors3 = validate_dataset_data(corrupt3, self.schema)
        self.assertFalse(is_valid3)
        self.assertTrue(any("boolean" in e.lower() or "not of type" in e.lower() for e in errors3))

    def test_zero_shipping_cost_passes(self):
        valid = copy.deepcopy(self.small_valid_data)
        valid["orders"][0]["shipping_costs"]["WH-01"] = 0.0
        is_valid, errors = validate_dataset_data(valid, self.schema)
        self.assertTrue(is_valid, f"Zero shipping cost should be valid: {errors}")

    def test_zero_stock_passes(self):
        valid = copy.deepcopy(self.small_valid_data)
        valid["warehouses"][0]["inventory"]["SKU-B"] = 0
        is_valid, errors = validate_dataset_data(valid, self.schema)
        self.assertTrue(is_valid, f"Zero stock should be valid: {errors}")

    def test_missing_route_is_valid(self):
        valid = copy.deepcopy(self.small_valid_data)
        del valid["orders"][0]["shipping_costs"]["WH-02"]
        is_valid, errors = validate_dataset_data(valid, self.schema)
        self.assertTrue(is_valid, f"Omitted route in shipping_costs should be valid: {errors}")

    def test_unsupported_schema_version_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["schema_version"] = "2.0"
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("schema_version" in e for e in errors))

    def test_empty_identifiers_fail(self):
        for collection, field in [
            ("skus", "sku_id"),
            ("warehouses", "warehouse_id"),
            ("orders", "order_id"),
        ]:
            corrupt = copy.deepcopy(self.small_valid_data)
            corrupt[collection][0][field] = ""
            is_valid, _ = validate_dataset_data(corrupt, self.schema)
            self.assertFalse(is_valid, f"Empty {field} should fail")

        corrupt_dataset_id = copy.deepcopy(self.small_valid_data)
        corrupt_dataset_id["dataset_id"] = ""
        is_valid, _ = validate_dataset_data(corrupt_dataset_id, self.schema)
        self.assertFalse(is_valid)

    def test_empty_names_fail(self):
        corrupt_sku = copy.deepcopy(self.small_valid_data)
        corrupt_sku["skus"][0]["name"] = ""
        is_valid, _ = validate_dataset_data(corrupt_sku, self.schema)
        self.assertFalse(is_valid)

        corrupt_wh = copy.deepcopy(self.small_valid_data)
        corrupt_wh["warehouses"][0]["name"] = ""
        is_valid, _ = validate_dataset_data(corrupt_wh, self.schema)
        self.assertFalse(is_valid)

    def test_zero_or_negative_order_quantity_fails(self):
        for quantity in (0, -3):
            corrupt = copy.deepcopy(self.small_valid_data)
            corrupt["orders"][0]["items"]["SKU-A"] = quantity
            is_valid, errors = validate_dataset_data(corrupt, self.schema)
            self.assertFalse(is_valid, f"Quantity {quantity} should fail")
            self.assertTrue(
                any("quantity" in e.lower() or "minimum" in e.lower() for e in errors)
            )

    def test_empty_order_items_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["orders"][0]["items"] = {}
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("items" in e for e in errors))

    def test_nested_missing_required_field_fails(self):
        corrupt_sku = copy.deepcopy(self.small_valid_data)
        del corrupt_sku["skus"][0]["name"]
        is_valid, _ = validate_dataset_data(corrupt_sku, self.schema)
        self.assertFalse(is_valid)

        corrupt_wh = copy.deepcopy(self.small_valid_data)
        del corrupt_wh["warehouses"][0]["capacity_orders"]
        is_valid, _ = validate_dataset_data(corrupt_wh, self.schema)
        self.assertFalse(is_valid)

        corrupt_order = copy.deepcopy(self.small_valid_data)
        del corrupt_order["orders"][0]["shipping_costs"]
        is_valid, _ = validate_dataset_data(corrupt_order, self.schema)
        self.assertFalse(is_valid)

    def test_nested_unknown_field_fails(self):
        corrupt_sku = copy.deepcopy(self.small_valid_data)
        corrupt_sku["skus"][0]["color"] = "red"
        is_valid, _ = validate_dataset_data(corrupt_sku, self.schema)
        self.assertFalse(is_valid)

        corrupt_wh = copy.deepcopy(self.small_valid_data)
        corrupt_wh["warehouses"][0]["opening_hours"] = "08:00-17:00"
        is_valid, _ = validate_dataset_data(corrupt_wh, self.schema)
        self.assertFalse(is_valid)

        corrupt_order = copy.deepcopy(self.small_valid_data)
        corrupt_order["orders"][0]["priority"] = 1
        is_valid, _ = validate_dataset_data(corrupt_order, self.schema)
        self.assertFalse(is_valid)

    def test_unknown_metadata_field_fails(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["metadata"]["created_at"] = "2026-11-11"
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)
        self.assertTrue(any("metadata" in e for e in errors))

    def test_duplicate_json_object_keys_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicate_keys.json"
            path.write_text(
                '{"schema_version": "1.0", "schema_version": "1.0"}',
                encoding="utf-8",
            )
            is_valid, errors = validate_file(path, self.schema)
            self.assertFalse(is_valid)
            self.assertTrue(any("Duplicate object key" in e for e in errors))

    def test_nan_and_infinity_shipping_costs_fail(self):
        for bad_cost in (float("nan"), float("inf"), float("-inf")):
            corrupt = copy.deepcopy(self.small_valid_data)
            corrupt["orders"][0]["shipping_costs"]["WH-01"] = bad_cost
            is_valid, errors = validate_dataset_data(corrupt, self.schema)
            self.assertFalse(is_valid, f"Non-finite cost {bad_cost!r} should fail")
            self.assertTrue(
                any("finite" in e.lower() or "not of type" in e.lower() for e in errors)
            )

    def test_policy_b_penalty_field_rejected(self):
        corrupt = copy.deepcopy(self.small_valid_data)
        corrupt["orders"][0]["penalty"] = 100.0
        is_valid, errors = validate_dataset_data(corrupt, self.schema)
        self.assertFalse(is_valid)

    def test_all_committed_fixtures_pass_structural_validation(self):
        fixtures = sorted(SAMPLES_DIR.glob("*.json"))
        self.assertGreaterEqual(len(fixtures), 10)
        for fixture in fixtures:
            is_valid, errors = validate_file(fixture, self.schema)
            self.assertTrue(is_valid, f"{fixture.name} failed validation: {errors}")


class TestDatasetGenerator(unittest.TestCase):
    """Tests for deterministic dataset generation."""

    def test_generator_determinism(self):
        ds1 = generate_dataset(num_warehouses=3, num_orders=10, num_skus=4, seed=12345)
        ds2 = generate_dataset(num_warehouses=3, num_orders=10, num_skus=4, seed=12345)
        self.assertEqual(json.dumps(ds1, sort_keys=True), json.dumps(ds2, sort_keys=True))

    def test_generator_different_seeds_produce_different_data(self):
        ds1 = generate_dataset(num_warehouses=3, num_orders=10, num_skus=4, seed=11111)
        ds2 = generate_dataset(num_warehouses=3, num_orders=10, num_skus=4, seed=22222)
        self.assertNotEqual(ds1, ds2)

    def test_generated_dataset_passes_validation(self):
        ds = generate_dataset(num_warehouses=4, num_orders=15, num_skus=5, seed=999)
        is_valid, errors = validate_dataset_data(ds)
        self.assertTrue(is_valid, f"Generated dataset failed validation: {errors}")

    def test_generated_dataset_is_feasible(self):
        ds = generate_dataset(num_warehouses=3, num_orders=8, num_skus=3, seed=777)
        res = check_dataset_feasibility(ds)
        self.assertEqual(res.status, FeasibilityStatus.FEASIBLE)

    def test_generator_invalid_arguments_raise(self):
        with self.assertRaises(ValueError):
            generate_dataset(num_warehouses=0, num_orders=5, num_skus=2, seed=1)
        with self.assertRaises(ValueError):
            generate_dataset(num_warehouses=2, num_orders=0, num_skus=2, seed=1)
        with self.assertRaises(ValueError):
            generate_dataset(num_warehouses=2, num_orders=5, num_skus=0, seed=1)

    def test_generator_output_file_is_valid_json(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            ds = generate_dataset(num_warehouses=2, num_orders=4, num_skus=2, seed=42)
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(ds, f)
            is_valid, errors = validate_file(tmp_path)
            self.assertTrue(is_valid, f"Written file invalid: {errors}")
        finally:
            if tmp_path.exists():
                tmp_path.unlink()

    def test_generator_cli_is_byte_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            outputs = [Path(tmp) / "first.json", Path(tmp) / "second.json"]
            for output in outputs:
                completed = subprocess.run(
                    [
                        sys.executable,
                        str(REPO_ROOT / "scripts" / "generate_dataset.py"),
                        "--warehouses", "4",
                        "--orders", "20",
                        "--skus", "5",
                        "--seed", "20261111",
                        "--output", str(output),
                    ],
                    cwd=REPO_ROOT,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(outputs[0].read_bytes(), outputs[1].read_bytes())
            self.assertEqual(json.loads(outputs[0].read_text(encoding="utf-8"))["metadata"]["seed"], 20261111)
            is_valid, errors = validate_file(outputs[0])
            self.assertTrue(is_valid, f"CLI-generated dataset invalid: {errors}")

    def test_generator_cli_rejects_invalid_arguments(self):
        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "scripts" / "generate_dataset.py"),
                    "--warehouses", "0",
                    "--orders", "5",
                    "--skus", "2",
                    "--seed", "1",
                    "--output", str(Path(tmp) / "invalid.json"),
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("num_warehouses", completed.stderr)
            self.assertFalse((Path(tmp) / "invalid.json").exists())

    def test_generated_datasets_are_feasible_across_seeds(self):
        for seed in (1, 17, 2026):
            dataset = generate_dataset(
                num_warehouses=3, num_orders=12, num_skus=4, seed=seed
            )
            result = check_dataset_feasibility(dataset)
            self.assertEqual(
                result.status,
                FeasibilityStatus.FEASIBLE,
                f"Generated seed {seed} was not feasible: {result.message}",
            )


class TestFeasibilityChecker(unittest.TestCase):
    """Tests for exhaustive small-instance feasibility search."""

    def test_sample_small_is_feasible(self):
        res = check_file(SAMPLES_DIR / "sample_small.json")
        self.assertEqual(res.status, FeasibilityStatus.FEASIBLE)
        self.assertIsNotNone(res.assignment)
        self.assertEqual(len(res.assignment), 3)

    def test_edge_tight_capacity_is_feasible(self):
        res = check_file(SAMPLES_DIR / "edge_tight_capacity.json")
        self.assertEqual(res.status, FeasibilityStatus.FEASIBLE)

    def test_edge_tight_inventory_is_feasible(self):
        res = check_file(SAMPLES_DIR / "edge_tight_inventory.json")
        self.assertEqual(res.status, FeasibilityStatus.FEASIBLE)

    def test_edge_equal_costs_is_feasible(self):
        res = check_file(SAMPLES_DIR / "edge_equal_costs.json")
        self.assertEqual(res.status, FeasibilityStatus.FEASIBLE)

    def test_edge_zero_stock_is_feasible(self):
        res = check_file(SAMPLES_DIR / "edge_zero_stock.json")
        self.assertEqual(res.status, FeasibilityStatus.FEASIBLE)
        self.assertEqual(res.assignment["ORD-001"], "WH-02")

    def test_edge_unavailable_route_is_feasible(self):
        res = check_file(SAMPLES_DIR / "edge_unavailable_route.json")
        self.assertEqual(res.status, FeasibilityStatus.FEASIBLE)
        self.assertEqual(res.assignment["ORD-001"], "WH-02")

    def test_sample_infeasible_is_infeasible(self):
        res = check_file(SAMPLES_DIR / "sample_infeasible.json")
        self.assertEqual(res.status, FeasibilityStatus.INFEASIBLE)

    def test_edge_infeasible_stock_is_infeasible(self):
        res = check_file(SAMPLES_DIR / "edge_infeasible_stock.json")
        self.assertEqual(res.status, FeasibilityStatus.INFEASIBLE)

    def test_state_limit_returns_unknown_not_infeasible(self):
        with open(SAMPLES_DIR / "sample_small.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        res = check_dataset_feasibility(data, max_states=1)
        self.assertEqual(res.status, FeasibilityStatus.UNKNOWN)

    def test_invalid_input_returns_invalid(self):
        corrupt = {"schema_version": "1.0", "policy": "B"}
        res = check_dataset_feasibility(corrupt)
        self.assertEqual(res.status, FeasibilityStatus.INVALID)

    def test_missing_file_returns_invalid(self):
        res = check_file(SAMPLES_DIR / "does_not_exist.json")
        self.assertEqual(res.status, FeasibilityStatus.INVALID)

    def test_all_fixtures_match_declared_feasibility_status(self):
        expected = {
            "sample_small.json": FeasibilityStatus.FEASIBLE,
            "sample_medium.json": FeasibilityStatus.FEASIBLE,
            "sample_large.json": FeasibilityStatus.FEASIBLE,
            "sample_infeasible.json": FeasibilityStatus.INFEASIBLE,
            "edge_tight_capacity.json": FeasibilityStatus.FEASIBLE,
            "edge_tight_inventory.json": FeasibilityStatus.FEASIBLE,
            "edge_equal_costs.json": FeasibilityStatus.FEASIBLE,
            "edge_zero_stock.json": FeasibilityStatus.FEASIBLE,
            "edge_unavailable_route.json": FeasibilityStatus.FEASIBLE,
            "edge_infeasible_stock.json": FeasibilityStatus.INFEASIBLE,
        }
        committed = {path.name for path in SAMPLES_DIR.glob("*.json")}
        self.assertEqual(committed, set(expected), "Fixture catalogue drifted from documented set")
        for filename, status in expected.items():
            result = check_file(SAMPLES_DIR / filename)
            self.assertEqual(
                result.status,
                status,
                f"{filename}: expected {status.value}, got {result.status.value} "
                f"({result.message})",
            )

    def test_omitted_routes_are_never_used(self):
        with open(SAMPLES_DIR / "edge_unavailable_route.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        result = check_dataset_feasibility(data)
        self.assertEqual(result.status, FeasibilityStatus.FEASIBLE)
        routes = {order["order_id"]: order["shipping_costs"] for order in data["orders"]}
        for order_id, warehouse_id in result.assignment.items():
            self.assertIn(
                warehouse_id,
                routes[order_id],
                f"Order {order_id} was assigned to an unavailable route {warehouse_id}",
            )

    def test_reported_total_cost_matches_assignment(self):
        with open(SAMPLES_DIR / "sample_small.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        result = check_dataset_feasibility(data)
        self.assertEqual(result.status, FeasibilityStatus.FEASIBLE)
        costs = {order["order_id"]: order["shipping_costs"] for order in data["orders"]}
        expected_cost = sum(
            costs[order_id][warehouse_id]
            for order_id, warehouse_id in result.assignment.items()
        )
        self.assertAlmostEqual(result.total_shipping_cost, expected_cost, places=6)

    def test_feasibility_checker_does_not_mutate_input(self):
        with open(SAMPLES_DIR / "sample_small.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        original_copy = copy.deepcopy(data)
        check_dataset_feasibility(data)
        self.assertEqual(data, original_copy)

    def test_feasible_assignment_satisfies_all_constraints(self):
        with open(SAMPLES_DIR / "sample_small.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        res = check_dataset_feasibility(data)
        self.assertEqual(res.status, FeasibilityStatus.FEASIBLE)
        assignment = res.assignment

        # 1. Every order assigned
        self.assertEqual(set(assignment.keys()), {o["order_id"] for o in data["orders"]})

        # 2. Capacity not exceeded
        wh_counts = {}
        for wid in assignment.values():
            wh_counts[wid] = wh_counts.get(wid, 0) + 1
        wh_map = {w["warehouse_id"]: w for w in data["warehouses"]}
        for wid, count in wh_counts.items():
            self.assertLessEqual(count, wh_map[wid]["capacity_orders"])

        # 3. Inventory not exceeded
        consumed = {wid: {} for wid in wh_map}
        for ord_item in data["orders"]:
            assigned_wh = assignment[ord_item["order_id"]]
            for sku, qty in ord_item["items"].items():
                consumed[assigned_wh][sku] = consumed[assigned_wh].get(sku, 0) + qty

        for wid, wh in wh_map.items():
            for sku, stock in wh["inventory"].items():
                used = consumed[wid].get(sku, 0)
                self.assertLessEqual(
                    used, stock, f"Warehouse {wid} exceeded stock for {sku}: used {used} > stock {stock}"
                )


class TestRepositoryRegression(unittest.TestCase):
    """Regression tests for existing files."""

    def test_legacy_benchmark_data_untouched(self):
        """Verify legacy prototype benchmark_data.json is preserved and unmodified."""
        path = REPO_ROOT / "benchmark_data.json"
        self.assertTrue(path.is_file(), "benchmark_data.json must exist")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("WH_THU_DUC", content)
        self.assertIn("ORD_2026_001", content)

    def test_validate_orders_script_exists(self):
        """Verify validate_orders.py legacy script is preserved."""
        path = REPO_ROOT / "validate_orders.py"
        self.assertTrue(path.is_file(), "validate_orders.py must exist")


if __name__ == "__main__":
    unittest.main()
