# Phân công & hạng mục bàn giao: LogiMind

> **Dự án:** LogiMind — Hệ thống tối ưu phân bổ và xử lý đơn hàng đa kho
> **Đội ngũ:** 6 vai trò chức năng
> **Lưu ý:** Danh tính thành viên, GitHub handle và deadline sprint được ghi là `TBD` cho đến khi được xác nhận chính thức.

---

## 1. Ma trận phân công vai trò

| Mã vai trò | Vai trò chức năng | Người phụ trách | GitHub handle | Deadline sprint | Trạng thái hiện tại |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TV1** | Phân tích nghiệp vụ & mô hình toán học | *TBD* | *TBD* | *TBD* | Đang lập kế hoạch |
| **TV2** | Dữ liệu & bộ dữ liệu kiểm thử | *TBD* | *TBD* | *TBD* | Đang lập kế hoạch |
| **TV3** | Thuật toán tối ưu | *TBD* | *TBD* | *TBD* | Đang lập kế hoạch |
| **TV4** | Frontend | *TBD* | *TBD* | *TBD* | Đang lập kế hoạch |
| **TV5** | Backend & cơ sở dữ liệu | *TBD* | *TBD* | *TBD* | Đang lập kế hoạch |
| **TV6** | Tích hợp, kiểm thử & báo cáo | *TBD* | *TBD* | *TBD* | Đang lập kế hoạch |

---

## 2. Đặc tả chi tiết từng vai trò

### TV1 — Phân tích nghiệp vụ & mô hình toán học

- **Phạm vi chính:**
  - Xây dựng bối cảnh nghiệp vụ, yêu cầu và ràng buộc logistics.
  - Định nghĩa chỉ số, biến quyết định, tham số, hàm mục tiêu và ràng buộc toán học.
  - Xác định chính sách phân bổ đơn (đã chọn Policy A) và xử lý trường hợp biên/không khả thi.
- **Hạng mục bàn giao chính:**
  - `docs/mathematical-model.md` (đặc tả hình thức).
  - Phần quy tắc nghiệp vụ trong `docs/requirements.md`.
  - Chứng minh bằng tính tay trên bài toán nhỏ.
- **Phụ thuộc:** Không (khởi tạo nền tảng mô hình).
- **Tiêu chí hoàn thành:**
  - Mô hình toán học được nhóm và giảng viên hướng dẫn xác nhận.
  - Toàn bộ ràng buộc và biến được TV3 xác nhận là giải được bằng máy tính.

---

### TV2 — Dữ liệu & bộ dữ liệu kiểm thử

- **Phạm vi chính:**
  - Thiết kế schema dữ liệu cho kho, SKU, mức tồn kho, dòng đơn hàng và ma trận chi phí vận chuyển.
  - Sinh bộ dữ liệu benchmark tổng hợp (nhỏ, vừa, lớn và các edge case bất thường).
  - Cung cấp file seed cơ sở dữ liệu và script nạp dữ liệu.
- **Hạng mục bàn giao chính:**
  - `docs/data-dictionary.md`.
  - `data/samples/` (bộ dữ liệu benchmark dạng JSON/CSV).
  - Script sinh dữ liệu và validator schema (`scripts/`).
- **Phụ thuộc:** TV1 (cần định nghĩa tham số toán học).
- **Tiêu chí hoàn thành:**
  - Bộ dữ liệu tuân thủ 100% schema trong từ điển dữ liệu.
  - Có ít nhất 1 benchmark khả thi và 1 edge case chắc chắn không khả thi.

---

### TV3 — Thuật toán tối ưu

- **Phạm vi chính:**
  - Cài đặt thuật toán heuristic Baseline (ví dụ: kho gần nhất, tham lam một kho).
  - Cài đặt mô hình tối ưu MILP bằng thư viện bộ giải Python (PuLP / OR-Tools / SciPy).
  - Đo thời gian chạy, khoảng cách tối ưu (optimality gap) và mức sử dụng kho.
- **Hạng mục bàn giao chính:**
  - Module thuật toán trong `src/logimind/algorithms/`.
  - Giao diện trừu tượng/adapter cho bộ giải.
  - Báo cáo so sánh benchmark (Baseline và MILP).
  - Unit test cho tính đúng đắn của tối ưu.
- **Phụ thuộc:** TV1 (mô hình toán học) và TV2 (bộ dữ liệu benchmark).
- **Tiêu chí hoàn thành:**
  - MILP đạt chi phí $\le$ Baseline trên các benchmark chuẩn.
  - Các bất biến được giữ nghiêm ngặt (không vi phạm tồn kho hoặc công suất).

---

### TV4 — Frontend

- **Phạm vi chính:**
  - Thiết kế và xây dựng giao diện cấu hình tình huống và trực quan hóa.
  - Cài đặt dashboard tổng hợp phân bổ (phân rã chi phí, mức sử dụng kho).
  - Trực quan hóa mức sử dụng công suất kho và tuyến gán đơn.
- **Hạng mục bàn giao chính:**
  - Ứng dụng web frontend trong `frontend/` (hoặc module UI).
  - Dashboard phân bổ và biểu đồ tương tác.
  - Bố cục responsive và phản hồi trạng thái lỗi rõ ràng.
- **Phụ thuộc:** TV5 (endpoint API và phản hồi mock).
- **Tiêu chí hoàn thành:**
  - Người dùng có thể chọn bộ dữ liệu, chạy phân bổ và xem kết quả trực quan mà không cần lệnh terminal.

---

### TV5 — Backend & cơ sở dữ liệu

- **Phạm vi chính:**
  - Xây dựng dịch vụ REST API quản lý bộ dữ liệu, điều phối các lần chạy bộ giải và trả kết quả.
  - Cài đặt lưu trữ quan hệ bằng SQLite.
  - Cài đặt kiểm tra dữ liệu đầu vào, xử lý lỗi và giới hạn thời gian chạy bộ giải.
- **Hạng mục bàn giao chính:**
  - Ứng dụng backend API trong `src/logimind/backend/`.
  - Model schema cơ sở dữ liệu và script migration.
  - Endpoint API chuẩn theo `docs/api-contract.md`.
- **Phụ thuộc:** TV3 (adapter thuật toán) và TV2 (schema dữ liệu).
- **Tiêu chí hoàn thành:**
  - Toàn bộ endpoint trong `docs/api-contract.md` được cài đặt, kiểm tra và vượt integration test.

---

### TV6 — Tích hợp, kiểm thử & báo cáo

- **Phạm vi chính:**
  - Thiết lập bộ kiểm thử tự động và cổng chất lượng CI.
  - Cài đặt integration test và regression suite giữa các module.
  - Đối chiếu hệ thống với yêu cầu chức năng.
  - Tổng hợp báo cáo benchmark và chuẩn bị slide/demo cho giảng viên.
- **Hạng mục bàn giao chính:**
  - Bộ kiểm thử trong `tests/` (unit, integration và end-to-end).
  - `docs/testing-strategy.md` và `docs/integration-guide.md`.
  - Báo cáo cuối kỳ và kịch bản demo.
- **Phụ thuộc:** TV1 đến TV5 (toàn bộ hạng mục bàn giao).
- **Tiêu chí hoàn thành:**
  - Tỷ lệ pass 100% trên bộ kiểm thử tự động trong CI.
  - Tổng duyệt thành công demo end-to-end trước buổi bảo vệ.
