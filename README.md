# LogiMind: Tối ưu phân bổ đơn hàng và quản lý kho bãi

Nền tảng tối ưu hóa phân phối đơn hàng giữa các kho dựa trên ràng buộc tồn kho (`capacity`), khoảng cách địa lý và năng lực xử lý thực tế, phục vụ cho các bài toán quy hoạch mạng lưới logistics thông minh.

## 🚀 Tính năng chính
- **Mô hình hóa dữ liệu kho & đơn hàng:** Quản lý tọa độ, sức chứa tối đa và trạng thái lưu trữ hiện tại của từng kho.
- **Kiểm tra ràng buộc tồn kho (Capacity Constraint):** Đảm bảo kho hàng không bị quá tải khi tiếp nhận đơn hàng mới.
- **Thuật toán phân bổ tối ưu:** Tự động tính toán khoảng cách không gian từ điểm giao hàng đến các kho khả dụng để chọn ra phương án tối ưu nhất.

## 📂 Cấu trúc thư mục dự án
```text
LogiMind/
│
├── benchmark_data.json    # Tập dữ liệu giả lập (Kho hàng & Đơn hàng)
├── validate_orders.py     # Script Python xử lý logic và kiểm tra ràng buộc
├── data-dictionary.md     # Tài liệu từ điển dữ liệu chi tiết
└── README.md              # Tài liệu hướng dẫn sử dụng dự án