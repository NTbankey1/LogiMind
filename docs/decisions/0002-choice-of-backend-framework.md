# ADR-002: Lựa chọn framework API backend

## Trạng thái

PROPOSED

## Bối cảnh

TV5 cần xây dựng dịch vụ backend để điều phối các lần chạy bộ giải, kiểm tra dữ liệu đầu vào, trả phản hồi API cho frontend của TV4 và lưu lịch sử phân bổ. Backend cần tích hợp liền mạch với các thư viện khoa học dữ liệu và tối ưu hóa của Python.

## Các phương án đã xem xét

1. **FastAPI (Python):**
   - *Ưu điểm:* Gọi trực tiếp module bộ giải Python trong cùng tiến trình (không có chi phí IPC); tự động sinh tài liệu OpenAPI/Swagger; tuần tự hóa nhanh qua Pydantic; sẵn sàng cho async.
   - *Nhược điểm:* Yêu cầu hiểu lập trình async trong Python, dù vẫn hỗ trợ endpoint đồng bộ.
2. **Flask (Python):**
   - *Ưu điểm:* Tối giản, rất quen thuộc với người mới học Python.
   - *Nhược điểm:* Không có kiểm tra schema request tích hợp; cần plugin thủ công để sinh tài liệu Swagger.
3. **Node.js (Express / NestJS):**
   - *Ưu điểm:* Thống nhất hệ sinh thái JavaScript với frontend.
   - *Nhược điểm:* Phải dùng IPC đa ngôn ngữ (spawn tiến trình Python hoặc microservice) để gọi bộ giải, làm tăng độ phức tạp cài đặt cho một dự án sinh viên.

## Quyết định (đề xuất)

Chọn **FastAPI** làm framework backend.

## Hệ quả

- **Tích cực:** Gọi trực tiếp các lớp bộ giải của TV3; tài liệu tương tác tự động tại `/docs`; định kiểu mạnh qua Pydantic.
- **Tiêu cực / Rủi ro:** TV5 cần làm quen với routing FastAPI và kiểm tra schema bằng Pydantic.
