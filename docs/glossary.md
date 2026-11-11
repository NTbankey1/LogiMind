# Thuật ngữ LogiMind

Tài liệu này quy định cách dùng thuật ngữ Việt–Anh thống nhất trong toàn bộ repository. Khi viết hoặc sửa tài liệu, dùng đúng các lựa chọn dưới đây.

---

## 1. Thuật ngữ nghiệp vụ và kỹ thuật

| Tiếng Anh | Cách dùng trong tài liệu tiếng Việt | Ghi chú |
| :--- | :--- | :--- |
| order | **đơn hàng** (lần đầu), sau đó **đơn** | Không dùng "đơn đặt hàng" xen kẽ. |
| order line / order item | **dòng đơn hàng** | |
| warehouse | **kho** | Không dùng "nhà kho" xen kẽ. |
| SKU | **SKU** | Giữ nguyên, không dịch. |
| inventory | **tồn kho** | |
| stock | **tồn kho** / **lượng hàng** | Phân biệt với `stock` là tên trường khi nói về schema. |
| capacity | **công suất** | Cụ thể: **công suất xử lý**. |
| `capacity_orders` | **`capacity_orders`** | Giữ nguyên tên trường; diễn giải là "công suất theo số đơn". |
| allocation | **phân bổ** | |
| assignment | **gán** | |
| solver | **bộ giải (solver)** lần đầu, sau đó **bộ giải** | |
| feasible | **khả thi** | |
| infeasible | **không khả thi** | |
| optimal | **tối ưu** | |
| optimality gap | **khoảng cách tối ưu (optimality gap)** | |
| baseline | **baseline** | Lần đầu: "phương án cơ sở (baseline)". |
| heuristic | **heuristic** | Có thể viết "thuật toán heuristic". |
| fixture | **fixture** | Lần đầu: "bộ dữ liệu mẫu (fixture)". |
| dataset | **bộ dữ liệu** | |
| split shipment | **giao tách đơn** | |
| unassigned order | **đơn chưa được phân bổ** / **đơn chưa gán** | |
| penalty | **penalty** | Giữ nguyên khi nói về trường/thành phần mô hình. |
| handling cost | **chi phí xử lý (handling cost)** | |
| utilization | **mức sử dụng** | |
| route | **tuyến** | |
| deterministic | **tất định** | |
| reproducibility | **khả năng tái lập** | |
| validation | **kiểm tra** / **kiểm chứng** | "Validate" dữ liệu là **kiểm tra**; "verify" là **kiểm chứng**. |
| test | **kiểm thử** (danh từ), **test** khi nói về mã/tên file | Giữ `test` trong tên file, lệnh và mã test. |
| unit test / integration test / E2E test | **unit test** / **integration test** / **E2E test** | Giữ nguyên thuật ngữ kỹ thuật. |
| contract | **hợp đồng** | Ví dụ: hợp đồng API, hợp đồng dữ liệu. |
| schema | **schema** | Giữ nguyên. |
| legacy | **legacy** | Lần đầu: "cũ (legacy)". |
| oracle | **bộ kiểm chứng (oracle)** | |
| edge case | **edge case** | Giữ nguyên. |
| blocker | **blocker** | Giữ nguyên. |
| gate | **cổng** | |
| handoff | **bàn giao** | |
| owner | **chủ sở hữu** | |
| acceptance criteria | **tiêu chí nghiệm thu** | |
| traceability | **truy vết** | |

---

## 2. Thuật ngữ công nghệ giữ nguyên

Không dịch các thuật ngữ sau: **API, Backend, Frontend, Database, REST, SQLite, MILP, LP, JSON, JSON Schema, Git, GitHub, CI, PR, Branch, Commit, Merge, Pull Request, Issue, ADR, FastAPI, React, Vite, Python, PuLP, OR-Tools, SciPy, Pydantic, SQLAlchemy, SQLModel, pytest, ruff, uvicorn, Docker**.

---

## 3. Tên trường và giá trị trong code

Luôn giữ nguyên trong dấu backtick:

- Trường dữ liệu: `order_id`, `warehouse_id`, `sku_id`, `quantity`, `capacity_orders`, `inventory`, `shipping_costs`, `shipping_cost`, `objective_value`, `items`.
- Trạng thái: `OPTIMAL`, `FEASIBLE`, `INFEASIBLE`, `NO_SOLUTION_FOUND`, `ERROR`, `UNKNOWN`, `INVALID`, `BASELINE_FAILED`.
- Lệnh, đường dẫn, tên file, endpoint: `python scripts/validate_dataset.py`, `data/samples/sample_small.json`, `POST /api/v1/allocations/run`.

---

## 4. Quy ước trình bày

1. Viết câu ngắn, chủ động, tránh văn phong quảng cáo.
2. Giữ cấu trúc tài liệu và số thứ tự mục ổn định để liên kết không bị hỏng.
3. Dùng bảng cho dữ liệu có cấu trúc; dùng danh sách cho quy trình.
4. Công thức toán học giữ nguyên ký hiệu gốc: $I$, $J$, $K$, $q_{ik}$, $s_{jk}$, $C_j$, $c_{ij}$, $x_{ij}$.
5. Không thêm tuyên bố về tính năng, kết quả kiểm thử hoặc trạng thái chưa có bằng chứng trong repository.
6. Không sửa nội dung chuyên môn của TV1 (yêu cầu, mô hình toán học) và TV2 (hợp đồng API, từ điển dữ liệu) khi chưa có xác nhận của chủ sở hữu.

---

## 5. Liên kết liên quan

- [Trung tâm tài liệu](index.md)
- [Chiến lược kiểm thử](testing-strategy.md)
- [Hợp đồng API](api-contract.md)
- [Từ điển dữ liệu](data-dictionary.md)
