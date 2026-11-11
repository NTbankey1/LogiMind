# ADR-001: Lựa chọn thư viện bộ giải tối ưu

## Trạng thái

PROPOSED

## Bối cảnh

LogiMind cần một engine tối ưu LP/MILP bằng Python để giải bài toán phân bổ đơn hàng đa kho. Bộ giải phải chạy ổn định trên laptop của từng thành viên, không cần giấy phép thương mại đắt tiền (như Gurobi hoặc CPLEX), đồng thời dễ cài đặt và dễ giảng dạy trong bối cảnh học thuật.

## Các phương án đã xem xét

1. **PuLP (backend Coin-OR CBC):**
   - *Ưu điểm:* Cú pháp Python đơn giản, dễ diễn đạt; đi kèm bộ giải CBC mặc định; là công cụ giảng dạy phổ biến trong các môn vận trù học; không rào cản giấy phép.
   - *Nhược điểm:* Chậm hơn trên các bài toán quy hoạch nguyên quy mô rất lớn (> 100.000 biến).
2. **Google OR-Tools:**
   - *Ưu điểm:* Backend C++ hiệu năng cao với binding Python; hỗ trợ bộ giải CP-SAT và GLOP/CBC; xử lý bài toán tổ hợp lớn tốt hơn.
   - *Nhược điểm:* Đường cong học tập cao hơn cho sinh viên khi mô hình hóa; cú pháp khác với mô hình đại số cổ điển.
3. **SciPy (`scipy.optimize.milp`):**
   - *Ưu điểm:* Có sẵn trong hệ sinh thái khoa học Python, dùng backend HiGHS.
   - *Nhược điểm:* Nhập ràng buộc ở mức ma trận, ít trực quan hơn khi mô hình hóa theo chỉ số đại số.

## Quyết định (đề xuất)

Chọn **PuLP** với backend CBC làm thư viện mô hình hóa chính cho baseline và mô hình MILP ban đầu của TV3, kèm adapter kiến trúc cho phép chuyển sang Google OR-Tools nếu gặp vấn đề về quy mô.

## Hệ quả

- **Tích cực:** Rào cản gia nhập thấp cho TV1 và TV3; dễ đọc, dễ trình bày trong báo cáo học thuật.
- **Tiêu cực / Rủi ro:** Các benchmark trên 10.000 đơn có thể cần điều chỉnh giới hạn thời gian giải.
