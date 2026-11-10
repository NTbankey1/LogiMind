# Data Dictionary - Dự án LogiMind

Tài liệu này định nghĩa cấu trúc dữ liệu chuẩn cho mô hình toán học và nền tảng tối ưu hóa phân bổ đơn hàng giữa các kho.

## 1. Thực thể Kho hàng (`warehouses`)
Mô tả thông tin về các kho hàng trong hệ thống mạng lưới logistics.

| Tên trường | Kiểu dữ liệu | Mô tả chi tiết |
| :--- | :--- | :--- |
| `warehouse_id` | String | Mã định danh duy nhất của kho (Ví dụ: `WH-01`) |
| `name` | String | Tên hiển thị của kho hàng |
| `location_code` | String | Mã định danh vùng địa lý của kho (Ví dụ: `NORTH`, `SOUTH`) |
| `daily_capacity` | Integer | Sức chứa hoặc năng lực xử lý đơn hàng tối đa trong ngày |
| `handling_cost_per_unit` | Float | Chi phí xử lý tính trên mỗi đơn vị sản phẩm tại kho |
| `inventory` | Object | Từ điển lưu số lượng tồn kho theo từng mã SKU (Ví dụ: `{"SKU-A": 10}`) |

---

## 2. Thực thể Đơn hàng (`orders`)
Mô tả thông tin các đơn hàng từ khách hàng cần được hệ thống tối ưu hóa phân bổ.

| Tên trường | Kiểu dữ liệu | Mô tả chi tiết |
| :--- | :--- | :--- |
| `order_id` | String | Mã định danh đơn hàng (Ví dụ: `ORD-001`) |
| `destination_zone` | String | Mã khu vực giao hàng của đơn hàng (Ví dụ: `ZONE-1`) |
| `items` | Object | Từ điển các sản phẩm và số lượng yêu cầu (Ví dụ: `{"SKU-A": 5}`) |
| `shipping_costs` | Object | Chi phí vận chuyển từ từng kho tới đơn hàng này (Ví dụ: `{"WH-01": 6.0, "WH-02": 11.0}`) |