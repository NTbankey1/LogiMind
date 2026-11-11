# Trung tâm tài liệu LogiMind

Chỉ mục tài liệu kỹ thuật và kiến trúc của hệ thống phân bổ đơn hàng đa kho **LogiMind**.

---

## 1. Danh mục tài liệu

| Tài liệu | Chủ sở hữu chính | Nội dung |
| :--- | :--- | :--- |
| [Tổng quan dự án](project-overview.md) | Toàn nhóm | Bối cảnh bài toán, phân tích nghiệp vụ, mục tiêu và giới hạn phạm vi. |
| [Yêu cầu hệ thống](requirements.md) | TV1 | Đặc tả yêu cầu chức năng (FR) và phi chức năng (NFR). |
| [Mô hình toán học](mathematical-model.md) | TV1 | Tập hợp, tham số, biến quyết định, ràng buộc, hàm mục tiêu và ví dụ. |
| [Kiến trúc hệ thống](architecture.md) | Project Lead & TV5 | Kiến trúc thành phần, giao tiếp giữa các module, lộ trình công nghệ và sơ đồ luồng. |
| [Hợp đồng API](api-contract.md) | TV2 | Schema yêu cầu/phản hồi Policy A, ngữ nghĩa trạng thái, quy tắc kiểm tra và mã lỗi. |
| [Từ điển dữ liệu](data-dictionary.md) | TV2 | Định nghĩa thực thể, kiểu trường, ràng buộc và phụ lục prototype cũ. |
| [Chiến lược kiểm thử](testing-strategy.md) | TV6 | Các bậc kiểm thử, kỳ vọng bao phủ, edge case và kiểm chứng tự động. |
| [Hướng dẫn tích hợp](integration-guide.md) | TV6 & Project Lead | Checklist bàn giao, phụ thuộc giữa các module và đồng bộ mốc tiến độ. |
| [Phân công thành viên](team-responsibilities.md) | Toàn nhóm | Vai trò TV1–TV6, hạng mục bàn giao, phụ thuộc và tiêu chí hoàn thành. |
| [Quy trình Git](git-workflow.md) | Project Lead | Mô hình nhánh, quy trình PR, quy ước commit và xử lý xung đột. |
| [Quyết định kiến trúc (ADR)](decisions/README.md) | Toàn nhóm | Ghi nhận các quyết định kiến trúc và lựa chọn công nghệ quan trọng. |
| [Thuật ngữ](glossary.md) | Project Lead | Bảng thuật ngữ Việt–Anh dùng thống nhất trong toàn bộ tài liệu. |

### Quản lý dự án và tài liệu tham khảo

| Tài liệu | Nội dung |
| :--- | :--- |
| [Trạng thái dự án](project-management/project-status.md) | Trạng thái TV1–TV6 dựa trên bằng chứng, blocker, rủi ro và minh chứng kiểm chứng. |
| [Theo dõi nhiệm vụ](project-management/task-tracker.md) | Checklist nhiệm vụ và ma trận phụ thuộc. |
| [Kế hoạch kiểm thử](project-management/test-plan.md) | Các bậc kiểm thử, edge case và trạng thái thực thi. |
| [Kế hoạch tích hợp](project-management/integration-plan.md) | Các mốc và kế hoạch đồng bộ giữa các module. |
| [Kế hoạch dọn dẹp repository](project-management/repository-cleanup-plan.md) | Kiểm kê, phân loại file, cấu trúc đích và kiểm chứng của đợt tái cấu trúc. |
| [Phân tích dự án (DOCX)](reference/project-analysis.docx) | Tài liệu phân tích học thuật và nghiệp vụ gốc bằng tiếng Việt. |

---

## 2. Lộ trình đọc theo vai trò

- **TV1 — Mô hình toán học:** bắt đầu tại [Mô hình toán học](mathematical-model.md) và [Yêu cầu hệ thống](requirements.md).
- **TV2 — Dữ liệu:** bắt đầu tại [Từ điển dữ liệu](data-dictionary.md) và [Chiến lược kiểm thử](testing-strategy.md).
- **TV3 — Thuật toán:** bắt đầu tại [Mô hình toán học](mathematical-model.md), [Từ điển dữ liệu](data-dictionary.md) và [Hợp đồng API](api-contract.md).
- **TV4 — Frontend:** bắt đầu tại [Hợp đồng API](api-contract.md) và [Kiến trúc hệ thống](architecture.md).
- **TV5 — Backend:** bắt đầu tại [Kiến trúc hệ thống](architecture.md), [Hợp đồng API](api-contract.md) và [Từ điển dữ liệu](data-dictionary.md).
- **TV6 — Kiểm thử & tích hợp:** bắt đầu tại [Chiến lược kiểm thử](testing-strategy.md), [Hướng dẫn tích hợp](integration-guide.md) và [Yêu cầu hệ thống](requirements.md).

---

## 3. Quy ước tài liệu

- Mỗi chủ đề có đúng một tài liệu chính thức; tài liệu khác chỉ liên kết, không chép lại.
- Thuật ngữ dùng theo [`glossary.md`](glossary.md).
- Không dịch tên biến, hàm, class, package, endpoint, đường dẫn, tên file và giá trị trạng thái trong code.
- Công thức, mô hình toán học và hợp đồng dữ liệu của TV1/TV2 chỉ được thay đổi bởi chủ sở hữu tương ứng.
