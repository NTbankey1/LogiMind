# Nhật ký thay đổi

Mọi thay đổi đáng chú ý của dự án **LogiMind** được ghi tại đây.

Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
dự án tuân theo [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Chưa phát hành]

### Thêm mới

- Khởi tạo dự án và cấu hình vệ sinh repository (`.gitignore`, `.editorconfig`, `.gitattributes`, `.env.example`).
- Kiến trúc tài liệu đầy đủ (`docs/`):
  - Tổng quan dự án và Yêu cầu (`project-overview.md`, `requirements.md`).
  - Đặc tả mô hình toán học (`mathematical-model.md`).
  - Kiến trúc hệ thống và sơ đồ luồng dữ liệu (`architecture.md`).
  - Hợp đồng API và schema chuẩn (`api-contract.md`).
  - Từ điển dữ liệu và schema trường (`docs/data-dictionary.md`).
  - Chiến lược kiểm thử và hướng dẫn tích hợp (`testing-strategy.md`, `integration-guide.md`).
  - Ma trận phân công và theo dõi tiến độ (`team-responsibilities.md`).
  - Quy trình nhánh Git và đóng góp (`git-workflow.md`, `CONTRIBUTING.md`).
  - Chỉ mục và mẫu Architecture Decision Record (`docs/decisions/`).
- Tự động hóa GitHub:
  - Workflow CI (`.github/workflows/ci.yml`) kiểm tra vệ sinh repository và tính toàn vẹn Markdown.
  - Mẫu Pull Request (`.github/pull_request_template.md`).
  - Mẫu issue cho báo lỗi, đề xuất tính năng và nhiệm vụ (`.github/ISSUE_TEMPLATE/`).
- README tạm cho các thư mục module (`src/`, `tests/`, `data/`, `scripts/`).
- Lớp dữ liệu Policy A của TV2:
  - JSON Schema chuẩn (`data/schema/dataset.schema.json`) và từ điển dữ liệu.
  - Mười fixture chuẩn và edge case trong `data/samples/`, kèm generator tất định, validator và bộ kiểm chứng khả thi vét cạn.
  - 60 test tự động và job CI kiểm tra dataset/feasibility của TV2.
  - ADR-004 lựa chọn Policy A.

### Thay đổi

- Căn chỉnh hợp đồng API, tổng quan dự án, kiến trúc, hướng dẫn tích hợp, chiến lược kiểm thử và README theo Policy A. Loại bỏ các trường split/penalty/handling khỏi ví dụ API và chuẩn hóa trạng thái bộ giải.
- Tổ chức lại cấu trúc repository:
  - Chuyển tài liệu phân tích học thuật sang `docs/reference/project-analysis.docx`.
  - Chuyển prototype cũ sang `scripts/validate_orders.py`, đọc dữ liệu tương đối theo `__file__` và nhận tham số dataset tùy chọn.
  - Chuyển fixture của prototype sang `data/legacy/benchmark_data.json`.
  - Gộp từ điển dữ liệu trùng ở thư mục gốc vào `docs/data-dictionary.md` thành Phụ lục A.
  - Đổi tên tài liệu quản lý dự án sang kebab-case.
- Cập nhật README, CLAUDE.md, CONTRIBUTING.md, liên kết tài liệu, đường dẫn kiến trúc và CI theo cấu trúc mới.
- Thêm bước CI chạy thử prototype phân bổ cũ.
- Việt hóa tài liệu hướng dẫn và quản lý dự án; chuẩn hóa thuật ngữ theo [`docs/glossary.md`](docs/glossary.md).

---

## [0.1.0] - 2026-10-29

- Khởi tạo repository và phát hành bộ tài liệu nền.
