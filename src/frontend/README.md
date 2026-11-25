# SmartAlloc Frontend Prototype

Prototype React/Vite cho đề tài **Hệ thống tối ưu phân bổ đơn hàng giữa nhiều kho**.

## Chạy local
1. Cài Node.js (khuyến nghị Node 20+).
2. Mở terminal tại thư mục dự án.
3. `npm install`
4. `npm run dev`
5. Mở URL Vite hiển thị trong terminal.

## Màn hình
- Dashboard
- Quản lý kho
- Đơn hàng
- Tối ưu phân bổ (so sánh baseline và heuristic)
- Mạng lưới kho
- Báo cáo
- Lịch sử (prototype)

## Lưu ý mô hình
Dữ liệu và chi phí là giả lập, để minh họa UI. Baseline chọn kho gần khu vực đơn nhất còn đủ tồn kho và công suất, theo thứ tự đơn. Heuristic mẫu ưu tiên đơn ưu tiên cao, lựa chọn kho theo chi phí khoảng cách cộng penalty sử dụng công suất. Đây là heuristic demo, không phải nghiệm tối ưu toán học được chứng minh. Chưa có backend/API và kết quả lịch sử chưa persist.
