# Cập nhật TV3 theo contract TV2

Chỉ chép `src/logimind`, `tests/algorithms`, `reports/optimization` vào checkout branch TV3. Xóa bản cũ `src/algorithms` và `tests/algorithms` trước khi chép (chỉ nếu là code TV3 cũ). Không ghi đè dữ liệu, docs hoặc scripts của TV1/TV2. `pyproject.toml` trong gói dựa trên main đã gửi; nếu branch có thay đổi khác, hợp nhất hai dòng bổ sung optimization và pythonpath thay vì ghi đè.

Từ root: `python -m pip install -e ".[optimization,dev]"`, `python -m pytest -q`, `python -m reports.optimization.benchmark`.

TV5: `from logimind.algorithms import optimize`; `optimize(dataset, "MILP", time_limit_seconds=30)` nhận nguyên JSON TV2. Kết quả là payload data API, TV5 bổ sung run_id, envelope và timestamp. Validator TV2 được gọi trực tiếp từ checkout; cần giữ scripts và data/schema tại root. SciPy/HiGHS được giữ từ phiên bản trước; ADR-001 đề xuất PuLP nhưng chưa chốt, cần nhóm xác nhận lựa chọn solver.

Kiểm thử: 23 test TV3 và 60 test TV2, tổng 83 pass. Benchmark 10 file TV2, 3 lần mỗi thuật toán. Không sửa dữ liệu TV2. Không có nghiệm đầy đủ thì allocations rỗng và chi phí null; gán tạm chỉ trong diagnostics. MIP gap trong diagnostics là tỷ lệ, không phải phần trăm.
