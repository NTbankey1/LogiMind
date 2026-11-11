# Thư mục mã nguồn: `src/`

Dành cho package ứng dụng Python. **Chưa có mã nguồn package.** Prototype cũ được cố ý giữ ngoài thư mục này tại [`scripts/validate_orders.py`](../scripts/validate_orders.py).

## Cấu trúc dự kiến

```text
src/
└── logimind/
    ├── __init__.py
    ├── algorithms/        # TV3: heuristic baseline, mô hình MILP, adapter bộ giải, chỉ số
    ├── backend/           # TV5: ứng dụng FastAPI, route, service, cấu hình
    └── data/              # TV2/TV5: model schema, bộ nạp dữ liệu, tiện ích lưu trữ
```

Frontend React + Vite là ứng dụng riêng trong `frontend/`. Không đặt frontend bên trong package Python.

## Quy tắc triển khai

1. **Chỉ tạo package khi có code thật.** Không commit `__init__.py` rỗng, module giả hoặc service tạm.
2. **Dependency:** thêm `pyproject.toml` khi package cần đóng gói, dependency runtime hoặc cấu hình công cụ. Không thêm chỉ để trang trí.
3. **Import:** dùng import tuyệt đối gốc `logimind` (ví dụ `from logimind.algorithms.baseline import allocate`).
4. **Hợp đồng:** dùng hợp đồng bộ dữ liệu Policy A chuẩn tại [`docs/data-dictionary.md`](../docs/data-dictionary.md) và hợp đồng API tại [`docs/api-contract.md`](../docs/api-contract.md). Không tự đặt tên trường hoặc quy tắc nghiệp vụ.
5. **Tất định:** nhận seed cố định và dùng quy tắc phá hòa được ghi rõ để các lần chạy benchmark tái lập được.
6. **Kiểm thử:** thêm unit test trong [`tests/unit/`](../tests/README.md) cùng Pull Request với phần cài đặt.

## Trạng thái hiện tại

`src/` chỉ chứa README này. TV3 (thuật toán), TV5 (backend) và mã truy cập dữ liệu dùng chung chưa được triển khai. Xem [`docs/architecture.md`](../docs/architecture.md) để biết sơ đồ thành phần đề xuất.
