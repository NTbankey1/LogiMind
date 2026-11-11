# ADR-003: Lựa chọn cơ sở dữ liệu lưu trữ cục bộ

## Trạng thái

PROPOSED

## Bối cảnh

TV5 cần lưu bộ dữ liệu benchmark, cấu hình kho và lịch sử các lần chạy phân bổ. Cơ sở dữ liệu phải dễ chạy cục bộ trên laptop của cả 6 thành viên, không cần quản trị server cơ sở dữ liệu riêng.

## Các phương án đã xem xét

1. **SQLite:**
   - *Ưu điểm:* Không cần cấu hình, lưu dạng file, tích hợp sẵn trong Python (`sqlite3`); không cần Docker hay dịch vụ cơ sở dữ liệu bên ngoài; nhẹ và hoàn toàn tất định.
   - *Nhược điểm:* Thông lượng ghi đồng thời hạn chế (không phải vấn đề với demo/đánh giá một người dùng).
2. **PostgreSQL:**
   - *Ưu điểm:* Đầy đủ tính năng cơ sở dữ liệu quan hệ cấp doanh nghiệp.
   - *Nhược điểm:* Cần cài dịch vụ PostgreSQL hoặc container Docker trên toàn bộ laptop của nhóm, tăng rào cản cài đặt.
3. **Mock trong bộ nhớ / file JSON:**
   - *Ưu điểm:* Cài đặt đơn giản nhất.
   - *Nhược điểm:* Không có khả năng truy vấn, toàn vẹn tham chiếu và cấu trúc quan hệ.

## Quyết định (đề xuất)

Chọn **SQLite** với ORM SQLAlchemy / SQLModel làm lớp lưu trữ cho LogiMind.

## Hệ quả

- **Tích cực:** Sẵn dùng trên mọi hệ điều hành; một file cơ sở dữ liệu duy nhất (`data/logimind.db`, đã được `.gitignore` bỏ qua).
- **Tiêu cực / Rủi ro:** Khi chuyển sang PostgreSQL trên môi trường cloud production sẽ cần cập nhật chuỗi kết nối và dialect của ORM.
