# Architecture Decision Records (ADR)

Thư mục này ghi lại các quyết định kỹ thuật và kiến trúc quan trọng của nhóm **LogiMind**.

---

## 1. ADR là gì?

Architecture Decision Record (ADR) ghi lại một quyết định kiến trúc quan trọng cùng bối cảnh, các phương án đã xem xét và hệ quả của quyết định.

---

## 2. Trạng thái ADR

- **PROPOSED:** Đang được nhóm xem xét, đánh giá.
- **ACCEPTED:** Đã được nhóm xác nhận và áp dụng.
- **REJECTED:** Đã xem xét nhưng không chọn.
- **SUPERSEDED:** Đã bị ADR sau thay thế.

---

## 3. Chỉ mục ADR

| Mã ADR | Tiêu đề | Ngày | Trạng thái | Chủ quyết định chính |
| :--- | :--- | :--- | :--- | :--- |
| [ADR-001](0001-choice-of-optimization-solver-library.md) | Lựa chọn thư viện bộ giải tối ưu (PuLP và OR-Tools) | 2026-10-29 | PROPOSED | TV3 & TV1 |
| [ADR-002](0002-choice-of-backend-framework.md) | Lựa chọn framework API backend (FastAPI) | 2026-10-29 | PROPOSED | TV5 |
| [ADR-003](0003-choice-of-database-engine.md) | Lựa chọn cơ sở dữ liệu lưu trữ cục bộ (SQLite) | 2026-10-29 | PROPOSED | TV5 |
| [ADR-004](0004-allocation-policy-a.md) | Áp dụng Policy A làm chính sách phân bổ đơn chuẩn | 2026-11-11 | ACCEPTED | TV2 & Project Lead |

---

## 4. Mẫu ADR

Để tạo ADR mới, sao chép cấu trúc sau vào `docs/decisions/XXXX-short-title.md`:

```markdown
# ADR-XXXX: [Tiêu đề ngắn]

## Status
[PROPOSED | ACCEPTED | REJECTED | SUPERSEDED]

## Context
Vấn đề hoặc câu hỏi kiến trúc cần giải quyết là gì? Có ràng buộc nào?

## Options Considered
1. **Phương án A:** [Ưu & nhược điểm]
2. **Phương án B:** [Ưu & nhược điểm]

## Decision
Chọn phương án nào và vì sao?

## Consequences
- **Tích cực:** Những lợi ích đạt được?
- **Tiêu cực / Rủi ro:** Những đánh đổi hoặc nợ kỹ thuật nào được chấp nhận?
```
