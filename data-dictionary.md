# Data Dictionary - Dự án LogiMind

Tài liệu này định nghĩa cấu trúc dữ liệu cho nền tảng tối ưu hóa phân bổ đơn hàng giữa các kho (`benchmark_data.json`).

## 1. Thực thể Kho hàng (`warehouses`)
Mô tả thông tin về các kho hàng trong hệ thống mạng lưới logistics.

| Tên trường | Kiểu dữ liệu | Mô tả chi tiết |
| :--- | :--- | :--- |
| `warehouse_id` | String | Mã định danh duy nhất của kho (Ví dụ: `WH_THU_DUC`) |
| `capacity` | Integer | Tổng sức chứa/năng lực xử lý tối đa của kho |
| `current_occupancy` | Integer | Số lượng hàng hóa hiện tại đang lưu trữ trong kho |
| `location.lat` | Float | Tọa độ vĩ độ (Latitude) của kho trên bản đồ |
| `location.lng` | Float | Tọa độ kinh độ (Longitude) của kho trên bản đồ |

---

## 2. Thực thể Đơn hàng (`orders`)
Mô tả thông tin các đơn hàng từ khách hàng cần được hệ thống tối ưu hóa phân bổ.

| Tên trường | Kiểu dữ liệu | Mô tả chi tiết |
| :--- | :--- | :--- |
| `order_id` | String | Mã định danh đơn hàng (Ví dụ: `ORD_2026_101`) |
| `items` | Array | Danh sách các sản phẩm trong đơn hàng |
| `items[].sku` | String | Mã SKU của sản phẩm |
| `items[].quantity` | Integer | Số lượng sản phẩm khách đặt mua |
| `destination.lat` | Float | Vĩ độ điểm giao hàng đích của đơn hàng |
| `destination.lng` | Float | Kinh độ điểm giao hàng đích của đơn hàng |