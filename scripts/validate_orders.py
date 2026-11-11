import argparse
import json
import math
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Location:
    lat: float
    lng: float

@dataclass
class Warehouse:
    warehouse_id: str
    capacity: int
    current_occupancy: int
    location: Location

    @property
    def remaining_capacity(self) -> int:
        return self.capacity - self.current_occupancy

@dataclass
class OrderItem:
    sku: str
    quantity: int

@dataclass
class Order:
    order_id: str
    items: List[OrderItem]
    destination: Location
    
    @property
    def total_quantity(self) -> int:
        return sum(item.quantity for item in self.items)


class LogisticsManager:
    """Quản lý và kiểm tra ràng buộc phân bổ đơn hàng cho hệ thống LogiMind."""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.warehouses: Dict[str, Warehouse] = {}
        self.orders: List[Order] = []

    def load_data(self) -> bool:
        """Đọc và load dữ liệu từ file JSON."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            
            # Load thông tin kho bãi
            for wh in raw_data.get("warehouses", []):
                loc = Location(**wh["location"])
                warehouse = Warehouse(
                    warehouse_id=wh["warehouse_id"],
                    capacity=wh["capacity"],
                    current_occupancy=wh["current_occupancy"],
                    location=loc
                )
                self.warehouses[warehouse.warehouse_id] = warehouse

            # Load thông tin đơn hàng
            for ord_data in raw_data.get("orders", []):
                loc = Location(**ord_data["destination"])
                items = [OrderItem(**item) for item in ord_data["items"]]
                self.orders.append(Order(
                    order_id=ord_data["order_id"],
                    items=items,
                    destination=loc
                ))

            print(f"✓ Đã tải thành công {len(self.warehouses)} kho hàng và {len(self.orders)} đơn hàng.")
            return True

        except FileNotFoundError:
            print(f"❌ Lỗi: Không tìm thấy file dữ liệu '{self.data_file}'.")
            return False
        except KeyError as e:
            print(f"❌ Lỗi: Thiếu trường dữ liệu bắt buộc {e}.")
            return False
        except Exception as e:
            print(f"❌ Lỗi không xác định khi đọc file: {e}")
            return False

    @staticmethod
    def calculate_distance(loc1: Location, loc2: Location) -> float:
        """Tính khoảng cách Euclidean cơ bản giữa 2 tọa độ (bán kính đơn giản)."""
        return math.sqrt((loc1.lat - loc2.lat) ** 2 + (loc1.lng - loc2.lng) ** 2)

    def validate_and_allocate(self):
        """Phân bổ đơn hàng vào kho gần nhất có đủ năng lực xử lý (Capacity Constraint)."""
        print("\n--- BẮT ĐẦU KIỂM TRA VÀ PHÂN BỔ ĐƠN HÀNG ---")
        
        for order in self.orders:
            print(f"\n📦 Đang xử lý đơn hàng: {order.order_id} (Tổng số lượng: {order.total_quantity})")
            
            # Sắp xếp các kho theo thứ tự khoảng cách từ kho tới điểm giao
            sorted_warehouses = sorted(
                self.warehouses.values(),
                key=lambda wh: self.calculate_distance(wh.location, order.destination)
            )

            allocated = False
            for wh in sorted_warehouses:
                if wh.remaining_capacity >= order.total_quantity:
                    # Cập nhật sức chứa kho
                    wh.current_occupancy += order.total_quantity
                    allocated = True
                    print(f"  ✓ Đã phân bổ thành công vào kho [{wh.warehouse_id}].")
                    print(f"    - Sức chứa còn lại của {wh.warehouse_id}: {wh.remaining_capacity}/{wh.capacity}")
                    break
                else:
                    print(f"  ⚠️ Kho [{wh.warehouse_id}] không đủ sức chứa (Còn lại: {wh.remaining_capacity}, Cần: {order.total_quantity}).")

            if not allocated:
                print(f"  ❌ THẤT BẠI: Không có kho nào đủ khả năng đáp ứng cho đơn hàng {order.order_id}!")

        print("\n--- HOÀN TẤT QUÁ TRÌNH PHÂN BỔ ---")


DEFAULT_DATA_FILE = (
    Path(__file__).resolve().parent.parent / "data" / "legacy" / "benchmark_data.json"
)


def main() -> int:
    """Run the legacy allocation prototype on the bundled benchmark data."""
    parser = argparse.ArgumentParser(
        description=(
            "Legacy LogiMind allocation prototype (nearest-warehouse heuristic). "
            "This is not the Policy A optimization engine."
        )
    )
    parser.add_argument(
        "data_file",
        nargs="?",
        default=str(DEFAULT_DATA_FILE),
        help=f"Prototype dataset path (default: {DEFAULT_DATA_FILE})",
    )
    args = parser.parse_args()

    manager = LogisticsManager(args.data_file)
    if manager.load_data():
        manager.validate_and_allocate()
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
