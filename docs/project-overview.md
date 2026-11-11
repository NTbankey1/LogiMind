# Tổng quan dự án: LogiMind

## 1. Tóm tắt

**LogiMind** là hệ thống hỗ trợ ra quyết định cho **bài toán phân bổ đơn hàng đa kho** (Multi-Warehouse Order Allocation Problem — MWOAP). Đơn hàng của khách được định tuyến tới các kho fulfillment dựa trên tồn kho theo từng SKU, công suất xử lý của kho và chi phí vận chuyển.

LogiMind mô hình hóa bài toán dưới dạng quy hoạch tuyến tính nguyên hỗn hợp (Mixed-Integer Linear Program — MILP), so sánh phương án tối ưu với các quy tắc heuristic baseline, và trình bày kết quả qua ứng dụng web cho nhân viên chuỗi cung ứng.

Chính sách phân bổ chuẩn là **Policy A — Strict Non-Split Allocation** ([ADR-004](decisions/0004-allocation-policy-a.md)):

- mỗi đơn hàng được giao đầy đủ;
- mỗi đơn hàng được gán cho đúng một kho;
- không cho phép giao tách đơn (split shipment);
- không cho phép đơn hàng chưa được phân bổ;
- không có split penalty, unassigned penalty hoặc handling cost;
- công suất kho được tính bằng **số đơn hàng**;
- tồn kho được theo dõi **riêng theo từng SKU**;
- hàm mục tiêu tối thiểu hóa tổng chi phí vận chuyển.

Nếu không tồn tại phương án phân bổ đầy đủ, bài toán **không khả thi về mặt toán học**; bộ dữ liệu vẫn hợp lệ về cấu trúc.

---

## 2. Bối cảnh nghiệp vụ & động lực

Các doanh nghiệp thương mại điện tử vận hành nhiều trung tâm fulfillment để giảm khoảng cách giao hàng. Vận hành đa kho tạo ra các đánh đổi:

1. **Phân mảnh tồn kho:** một đơn chứa nhiều SKU có thể không đủ hàng tại kho gần nhất.
2. **Giao từ một kho:** Policy A yêu cầu giao toàn bộ đơn từ một kho, nên kho chỉ đủ điều kiện khi có đủ số lượng của mọi SKU trong đơn.
3. **Nghẽn công suất:** dồn mọi đơn về kho gần nhất có thể làm cạn công suất xử lý và buộc các đơn sau phải đi tuyến đắt hơn.
4. **Chi phí vận chuyển và công suất:** một kho rẻ hơn có thể hết công suất hoặc hết hàng, nên bộ giải phải xét toàn bộ lô đơn thay vì chọn kho gần nhất cho từng đơn một cách độc lập.

LogiMind cân bằng các yếu tố này để tối thiểu hóa tổng chi phí vận chuyển trong khi tôn trọng tồn kho theo SKU và công suất theo số đơn. Giao tách đơn, phí xử lý và penalty cho đơn chưa phân bổ nằm ngoài chính sách hiện hành và không được tối ưu.

---

## 3. Mục tiêu cốt lõi

1. **Mô hình hóa:** cài đặt mô hình MILP Policy A trong [docs/mathematical-model.md](mathematical-model.md).
2. **Benchmark:** so sánh heuristic baseline tất định với MILP trên cùng bộ dữ liệu chuẩn; báo cáo tổng chi phí vận chuyển, số đơn được gán, mức sử dụng và thời gian chạy.
3. **Dữ liệu thực tế:** cung cấp bộ dữ liệu tổng hợp tái lập được trong `data/samples/`, được kiểm tra theo [data/schema/dataset.schema.json](../data/schema/dataset.schema.json).
4. **Trực quan hóa tương tác:** cho phép người vận hành chọn bộ dữ liệu, chạy phân bổ và xem một kho cho mỗi đơn, chi phí và mức sử dụng công suất.
5. **Chuẩn học thuật:** duy trì khả năng tái lập, kiểm thử tự động và một hợp đồng dữ liệu chính thức duy nhất.

---

## 4. Phạm vi dự án

### Trong phạm vi

- Phân bổ đơn hàng đa kho trong một cửa sổ lập kế hoạch fulfillment.
- Đơn hàng một SKU và nhiều SKU.
- Tồn kho theo từng SKU và công suất kho theo số đơn.
- Chi phí vận chuyển đơn–kho được tính trước.
- Các trạng thái Policy A: `OPTIMAL`, `FEASIBLE`, `INFEASIBLE`, `NO_SOLUTION_FOUND`, `ERROR`.
- Chỉ số so sánh: tổng chi phí vận chuyển, số đơn được gán, mức sử dụng kho và thời gian tính toán.

### Ngoài phạm vi (tạm hoãn)

- Giao tách đơn, phí xử lý và penalty cho đơn chưa phân bổ (không thuộc Policy A).
- Định tuyến đội xe thời gian thực và chỉ đường từng chặng.
- Bổ sung tồn kho dài hạn và dự báo nhu cầu.
- Định giá động và đàm phán API với hãng vận chuyển.

---

## 5. Tài liệu chính thức

| Chủ đề | Tài liệu |
| :--- | :--- |
| Mô hình toán học | [mathematical-model.md](mathematical-model.md) |
| Yêu cầu hệ thống | [requirements.md](requirements.md) |
| Hợp đồng bộ dữ liệu | [data-dictionary.md](data-dictionary.md) |
| Giao diện API | [api-contract.md](api-contract.md) |
| Phương pháp kiểm thử | [testing-strategy.md](testing-strategy.md) |
| Quyết định chính sách | [ADR-004](decisions/0004-allocation-policy-a.md) |
| Thuật ngữ | [glossary.md](glossary.md) |
