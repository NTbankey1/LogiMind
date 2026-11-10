import json

def validate_orders(filepath="benchmark_data.json"):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"=== Đang kiểm tra Dataset: {data.get('name')} ===")
        
        # Đọc danh sách kho hàng
        warehouses = {wh["warehouse_id"]: wh for wh in data.get("warehouses", [])}
        print(f"✓ Đã nạp {len(warehouses)} kho hàng thành công.")
        
        # Đọc danh sách đơn hàng
        orders = data.get("orders", [])
        print(f"✓ Đã nạp {len(orders)} đơn hàng thành công.\n")
        
        # Duyệt qua từng đơn hàng để kiểm tra tính khả thi và chi phí tối ưu
        for order in orders:
            order_id = order["order_id"]
            zone = order["destination_zone"]
            items = order["items"] # Dạng dict: {"SKU-A": 5}
            shipping_costs = order["shipping_costs"] # Dạng dict: {"WH-01": 6.0, ...}
            
            print(f"📦 Đang xử lý đơn hàng: {order_id} tại {zone}")
            print(f"   - Sản phẩm yêu cầu: {items}")
            
            best_wh = None
            min_total_cost = float('inf')
            
            # Kiểm tra xem kho nào đủ điều kiện (tồn kho & sức chứa) và có chi phí thấp nhất
            for wh_id, ship_cost in shipping_costs.items():
                wh = warehouses.get(wh_id)
                if not wh:
                    continue
                
                # Kiểm tra ràng buộc tồn kho cho tất cả SKU trong đơn hàng
                can_fulfill = True
                total_units = 0
                for sku, req_qty in items.items():
                    total_units += req_qty
                    avail_qty = wh["inventory"].get(sku, 0)
                    if avail_qty < req_qty:
                        can_fulfill = False
                        break
                
                # Kiểm tra ràng buộc sức chứa ngày (daily_capacity)
                if can_fulfill and wh["daily_capacity"] >= total_units:
                    # Tổng chi phí = Chi phí vận chuyển + (Số lượng * Phí xử lý đơn vị)
                    handling_cost = total_units * wh["handling_cost_per_unit"]
                    total_cost = ship_cost + handling_cost
                    
                    if total_cost < min_total_cost:
                        min_total_cost = total_cost
                        best_wh = wh_id
            
            if best_wh:
                print(f"   -> 🟢 Phân bổ thành công vào kho: [{best_wh}] | Tổng chi phí ước tính: {min_total_cost}\n")
            else:
                print(f"   -> 🔴 CẢNH BÁO: Không có kho nào đủ tồn kho hoặc sức chứa đáp ứng đơn hàng {order_id}!\n")

        print("✨ Quá trình kiểm tra validator hoàn tất!")
        return True

    except Exception as e:
        print(f"❌ Lỗi thực thi validator: {e}")
        return False

if __name__ == "__main__":
    validate_orders("benchmark_data.json")