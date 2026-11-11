# Trạng thái dự án LogiMind

> **Chủ sở hữu:** Project Lead / TV6
> **Kiểm chứng lần cuối:** 2026-11-11 (Asia/Ho_Chi_Minh)
> **Baseline:** `main` tại commit `f7f5862`
> **Phạm vi:** Các thay đổi chưa commit trong working tree **không** được tính là hạng mục bàn giao. Số liệu GitHub bên dưới được đọc trực tiếp từ repository trong ngày kiểm chứng.

---

## 1. Giai đoạn hiện tại

LogiMind đang ở giai đoạn **xây dựng nền tảng dữ liệu, đặc tả hệ thống và prototype**. Repository đã có tài liệu, workflow CI, prototype Python độc lập, lớp dữ liệu Policy A của TV2 (schema, mười fixture, validator, generator, bộ kiểm chứng khả thi và 60 test). Repository **chưa** có engine tối ưu, backend, tầng cơ sở dữ liệu hay frontend được triển khai.

| Khu vực | Trạng thái hiện tại | Minh chứng |
| :--- | :--- | :--- |
| Nền tảng repository | Đã khởi tạo | PR #1; commit `cb5f5ad` |
| Yêu cầu và mô hình toán học | Đã chọn Policy A; tài liệu đã có | PR #5; [requirements](../requirements.md), [mathematical model](../mathematical-model.md), [ADR-004](../decisions/0004-allocation-policy-a.md) |
| Kiến trúc và hợp đồng API | Đã căn chỉnh Policy A; chưa có cài đặt | [architecture](../architecture.md), [api-contract](../api-contract.md); ADR-001/002/003 vẫn `PROPOSED` |
| Lớp dữ liệu | TV2 đã triển khai và merge (PR #11, #13) | [schema](../../data/schema/dataset.schema.json), [data dictionary](../data-dictionary.md), mười fixture trong `data/samples/`; prototype cũ trong `data/legacy/` |
| Engine tối ưu | Chưa bắt đầu trong `src/` | Chỉ có prototype cũ `scripts/validate_orders.py` |
| Backend và SQLite | Chưa bắt đầu | Không có mã backend hoặc migration |
| Frontend | Chưa bắt đầu | Không có mã frontend hoặc package manifest |
| Kiểm thử tự động | TV2 đã triển khai và merge | [tests/test_datasets.py](../../tests/test_datasets.py), 60 test pass; xem [tests/README.md](../../tests/README.md) |
| CI | Hai job: vệ sinh repository và dataset/feasibility của TV2 | [.github/workflows/ci.yml](../../.github/workflows/ci.yml) |
| Theo dõi nhiệm vụ | Chưa thiết lập | 0 GitHub Issue, 0 milestone |
| Tích hợp | Chưa bắt đầu | Chưa có giao diện module nào được cài đặt |

---

## 2. Tiến độ đã kiểm chứng của TV1–TV6

Từ vựng trạng thái: **Completed**, **In Progress**, **Blocked**, **Not Started**, **Unable to Verify**.
Quyền sở hữu vai trò theo [team-responsibilities](../team-responsibilities.md). Danh tính thành viên, GitHub handle và deadline vẫn là `TBD`; do đó tác giả commit/PR **không** được ánh xạ tự động sang vai trò.

| Thành viên | Trách nhiệm | Hạng mục đã kiểm chứng | Hạng mục còn thiếu | Trạng thái | Minh chứng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TV1** | Yêu cầu nghiệp vụ và mô hình toán học | `docs/requirements.md` và `docs/mathematical-model.md` với tập hợp, tham số, ràng buộc, pseudocode baseline và ví dụ Policy A | Nhóm xác nhận Policy A; chốt các câu hỏi tham số/lưu trữ còn lại và sign-off với TV2/TV3/TV5 | **In Progress** | PR #5 (merge 2026-11-02): <https://github.com/NTbankey1/LogiMind/pull/5>; [model §3](../mathematical-model.md); [requirements §3](../requirements.md) |
| **TV2** | Bộ dữ liệu và kiểm thử dữ liệu | [Schema](../../data/schema/dataset.schema.json) và [từ điển dữ liệu](../data-dictionary.md) Policy A; mười fixture benchmark/edge case; generator tất định, validator và bộ kiểm chứng khả thi; [test tự động](../../tests/test_datasets.py); job CI TV2 | Bổ sung fixture cho kịch bản mới khi cần | **Completed** | PR #11 và #13 (đã merge); [data/README.md](../../data/README.md); [scripts/README.md](../../scripts/README.md); [ADR-004](../decisions/0004-allocation-policy-a.md) |
| **TV3** | Thuật toán tối ưu | Không có trong vị trí được giao. Prototype cũ `scripts/validate_orders.py` (kho gần nhất, công suất tổng) không gắn với TV3. | Package baseline, mô hình MILP, adapter bộ giải, chỉ số, unit test, báo cáo benchmark trong `src/logimind/algorithms/` | **Not Started** | `src/` chỉ có [README](../../src/README.md); [integration-guide](../integration-guide.md) mô tả adapter dự kiến |
| **TV4** | Frontend | Không có | Ứng dụng UI, so sánh chi phí, mức sử dụng công suất, trạng thái lỗi, tích hợp API, luồng E2E | **Not Started** | Không có file frontend hoặc package manifest |
| **TV5** | Backend và cơ sở dữ liệu | Không có | Dịch vụ FastAPI, schema/migration SQLite, endpoint, kiểm tra dữ liệu, xử lý timeout, integration test | **Not Started** | `src/` chỉ có README; ADR-002 và ADR-003 vẫn `PROPOSED` ([ADR index](../decisions/README.md)) |
| **TV6** | Tích hợp, kiểm thử tổng thể, báo cáo | [testing-strategy](../testing-strategy.md); [integration-guide](../integration-guide.md); workflow CI; bộ 60 test và job dataset/feasibility của TV2; bộ tài liệu quản lý dự án này | Test ứng dụng TV3/TV5; test hợp đồng/tích hợp/E2E; required status check; quy trình bug tracking; báo cáo benchmark; báo cáo/demo cuối kỳ | **In Progress** (tài liệu + test TV2) | [.github/workflows/ci.yml](../../.github/workflows/ci.yml); [tests/test_datasets.py](../../tests/test_datasets.py); [testing-strategy §4](../testing-strategy.md) |

### Sự thật đã kiểm chứng và điều chưa xác định

**Đã kiểm chứng**

- `main` không có cài đặt `src/logimind/algorithms`, `src/logimind/backend` hay `frontend`; chỉ có README tạm.
- `tests/` chứa bộ test TV2; `scripts/` chứa prototype cũ cùng validator, generator và bộ kiểm chứng khả thi của TV2.
- `pyproject.toml` tồn tại (cấu hình build, extra `data`/`dev`, cấu hình pytest và ruff).
- `.gitignore` bỏ qua `.env`, `*.db`, `*.sqlite`, `*.sqlite3`, `data/raw/`, `data/processed/` và các thư mục cache.
- CI có hai job: vệ sinh repository (JSON, smoke prototype, liên kết Markdown, file thiết yếu) và TV2 dataset/feasibility (validator, 60 test, trạng thái kỳ vọng, tính tất định của generator).
- Tại thời điểm kiểm chứng: **60 test pass**, **10/10 fixture hợp lệ với 0 lỗi**, **0 liên kết nội bộ hỏng**.
- GitHub có **13 PR**: #1, #2, #4, #5, #6, #7, #9, #10, #11, #12, #13 đã merge; #3 và #8 đã đóng. **0 Issue** và **0 milestone**.
- PR #11 và #13 đã merge lớp dữ liệu Policy A và căn chỉnh tài liệu.

**Chưa xác định từ repository**

- Tài khoản GitHub tương ứng với từng vai trò TV1–TV6.
- Công việc ngoài repository, nỗ lực cá nhân thực tế hoặc deadline.
- Chủ sở hữu dự kiến của prototype cũ (`scripts/validate_orders.py`), fixture (`data/legacy/benchmark_data.json`) và từ điển dữ liệu (`docs/data-dictionary.md`).
- Ngày sprint và định nghĩa milestone.

---

## 3. Hạng mục đã hoàn thành và còn thiếu

### Đã hoàn thành (artifact tồn tại; chưa nhất thiết được nghiệm thu)

| Hạng mục | Vị trí | Kiểm chứng |
| :--- | :--- | :--- |
| Khung repository, chỉ mục tài liệu, workflow CI, mẫu PR/issue | Thư mục gốc và `.github/` | PR #1; commit `cb5f5ad` |
| Yêu cầu hệ thống | [docs/requirements.md](../requirements.md) | PR #5; đã merge |
| Mô hình toán học | [docs/mathematical-model.md](../mathematical-model.md) | PR #5; đã merge |
| Cập nhật kiến trúc và luồng dữ liệu | [docs/architecture.md](../architecture.md) | PR #4; đã merge |
| Tài liệu phân tích dự án | [`docs/reference/project-analysis.docx`](../reference/project-analysis.docx) | PR #2; đã merge; được chuyển từ thư mục gốc trong đợt dọn dẹp |
| Script phân bổ prototype | [scripts/validate_orders.py](../../scripts/validate_orders.py) | Commit `7424ba4`; đã chạy smoke |
| Bộ dữ liệu benchmark và schema cũ | `data/legacy/benchmark_data.json`, [Phụ lục A](../data-dictionary.md#appendix-a-legacy-prototype-dataset-specification) | Đã tách khỏi fixture Policy A |
| Schema và fixture Policy A chuẩn | [data/schema/dataset.schema.json](../../data/schema/dataset.schema.json), `data/samples/` | PR #11; đã merge |
| Validator, generator, bộ kiểm chứng khả thi, test của TV2 | [scripts/README.md](../../scripts/README.md), [tests/test_datasets.py](../../tests/test_datasets.py) | PR #11; đã merge; 60 test pass |
| Fixture benchmark mẫu | [data/samples/sample_small.json](../../data/samples/sample_small.json) | Commit khởi tạo `cb5f5ad`, đã được thay thế bằng fixture chuẩn |
| Kiểm tra vệ sinh CI | [.github/workflows/ci.yml](../../.github/workflows/ci.yml) | Hai job đã cấu hình |
| Viết lại quy trình đóng góp | PR #6 | Đã merge |
| Việt hóa tài liệu hướng dẫn và quản lý dự án | Nhánh `docs/vietnamese-documentation` | Đang thực hiện; chưa commit |

### Còn thiếu

- Nhóm xác nhận chính thức Policy A và các quyết định tham số còn lại.
- Package baseline và bộ giải MILP.
- Adapter bộ giải với hợp đồng đầu vào/đầu ra ổn định.
- Backend FastAPI, schema/migration SQLite và cài đặt API.
- Ứng dụng frontend và tích hợp API.
- Unit test, contract test, integration test, system test và E2E test cho TV3/TV5/TV4.
- Required status check CI và quy trình bug tracking.
- Báo cáo benchmark, báo cáo cuối kỳ và minh chứng demo.

---

## 4. Blocker và phụ thuộc

| ID | Blocker | Công việc bị ảnh hưởng | Phụ thuộc / chủ sở hữu | Minh chứng hiện tại |
| :--- | :--- | :--- | :--- | :--- |
| B-01 | Quyết định Policy A cần nhóm xác nhận và các module hạ nguồn áp dụng | Schema TV2, bộ giải TV3, API TV5, UI TV4, test TV6 | TV1/Project Lead; TV3/TV4/TV5 | Policy A đã ghi tại [ADR-004](../decisions/0004-allocation-policy-a.md); hợp đồng chuẩn tại [data-dictionary.md](../data-dictionary.md) |
| B-02 | Không có schema dữ liệu chuẩn | Fixture TV2, đầu vào TV3, lưu trữ TV5, test TV6 | TV2 sau B-01 | **Đã giải quyết cho TV2** bằng [schema](../../data/schema/dataset.schema.json) và [từ điển](../data-dictionary.md); việc TV3/TV5/TV6 áp dụng vẫn mở. |
| B-03 | Hợp đồng API đã căn chỉnh nhưng chưa cài đặt/sign-off | Frontend TV4, backend TV5, contract test TV6 | TV1, TV3, TV4, TV5 | [api-contract.md](../api-contract.md) đã căn chỉnh Policy A; chưa có backend |
| B-04 | Chưa có adapter/cài đặt bộ giải | Tích hợp backend TV5, integration test TV6 | TV3 | [integration-guide](../integration-guide.md) nêu `solve_allocation(...)`, nhưng chưa có code |
| B-05 | Chưa có backend hoặc cơ sở dữ liệu | Tích hợp UI TV4, API/E2E test TV6 | TV5 | `src/` chỉ có README; ADR-002/003 `PROPOSED` |
| B-06 | Chưa có frontend | E2E test TV6 | TV4 | Không có file frontend |
| B-07 | Thiếu test ứng dụng TV3/TV5 và required CI status check (bộ 60 test TV2 đã có) | Minh chứng nghiệm thu và phát hành | TV6 cùng chủ sở hữu module | [testing-strategy §4](../testing-strategy.md); [.github/workflows/ci.yml](../../.github/workflows/ci.yml) |
| B-08 | Chưa có quyền sở hữu nhiệm vụ hoặc lịch sử issue | Điều phối và theo dõi tiến độ | Project Lead | 0 Issue, 0 milestone; roster `TBD` trong [team-responsibilities](../team-responsibilities.md) |

> **Cập nhật 2026-11-11:** Policy A đã được ghi tại [ADR-004](../decisions/0004-allocation-policy-a.md). Schema và từ điển TV2 giải quyết B-02 cho TV2; việc TV3/TV5/TV6 áp dụng vẫn mở.

---

## 5. Sổ rủi ro

| ID | Mô tả | Mức độ | Ảnh hưởng | Phụ thuộc | Đề xuất giảm thiểu | Vai trò phụ trách |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | Policy A đã chọn nhưng chưa được mọi module xác nhận/áp dụng | High | Cài đặt không tương thích nếu một module giữ hành vi trước Policy A | TV1/Project Lead; TV3/TV4/TV5 | Ghi nhận xác nhận của nhóm; theo dõi việc áp dụng trong project-status và review PR | TV1 / Project Lead |
| **R-02** | Schema chuẩn đã công bố nhưng chưa được mọi module dùng | High | Bộ giải/API/UI lệch nhau và fixture không hợp lệ | B-01, TV2 | Dùng `data/schema/dataset.schema.json`; chạy `scripts/validate_dataset.py` trong test module | TV2, TV3, TV5 |
| **R-03** | Chưa có cài đặt ở vị trí của TV3, TV4, TV5 | High | Dự án không thể tích hợp hoặc demo | Chủ sở hữu module | Tạo milestone với tiêu chí nghiệm thu; báo cáo tiến độ qua PR | TV3, TV4, TV5 |
| **R-04** | Ngữ nghĩa API/mô hình/trạng thái chưa được cài đặt/sign-off | High | Lỗi tích hợp; contract test fail | B-03 | Cài đặt hợp đồng API Policy A; lấy sign-off TV1/TV3/TV4/TV5 | TV1, TV3, TV4, TV5 |
| **R-05** | Chưa có test TV3/TV5; chỉ có test TV2 | High | Không phát hiện regression của bộ giải/API | TV6, chủ sở hữu module | Thêm unit/integration/E2E test; đưa job TV2 thành required status check | TV6, TV3, TV5 |
| **R-06** | Không có Issue/milestone/assignee | High | Không nhìn thấy tiến độ và trách nhiệm; blocker kéo dài | Project Lead | Tạo sáu issue workstream với tiêu chí nghiệm thu và phụ thuộc | Project Lead |
| **R-07** | ~~`.gitignore` cho phép `.env`, database, dữ liệu thô~~ | ~~High~~ | ~~Rò rỉ secret; phình repository~~ | — | **Đã xử lý:** `.gitignore` hiện bỏ qua `.env`, `*.db`, `*.sqlite`, `*.sqlite3`, `data/raw/`, `data/processed/` | Project Lead |
| **R-08** | Ruleset có bypass actor và chưa có required status check | Medium–High | Có thể bỏ qua phê duyệt/CI, giảm bảo vệ | Project Lead | Xem lại danh sách bypass; yêu cầu CI check; bật last-push approval | Project Lead |
| **R-09** | Push trực tiếp và regression tài liệu trên `main` | Medium | Thay đổi không được theo dõi; mất tài liệu; quyền sở hữu không rõ | Project Lead | Thực thi quy trình PR-only; thêm bước audit cho push trực tiếp | Project Lead |
| **R-10** | Lệch tài liệu: từ điển trùng, README cũ, tuyên bố ADR/dữ liệu sai | Medium | Người đóng góp làm theo quy tắc sai; lỗi tích hợp | TV1, TV2, TV6 | Hợp nhất từ điển; sửa tuyên bố README/ADR; thêm kiểm tra liên kết/nội dung | TV2 / TV6 |
| **R-11** | Prototype bị nhầm với baseline/MILP tài liệu hóa | Medium | Tự tin sai; so sánh benchmark sai | TV3, TV6 | Dán nhãn prototype rõ ràng; giữ ngoài minh chứng nghiệm thu cho đến khi đúng mô hình | TV3 / TV6 |
| **R-12** | `sample_small.json` không khớp ví dụ trong mô hình | Medium | Test và tính tay không thống nhất | TV2 | Tái sinh hoặc sửa fixture theo ví dụ đã duyệt | TV2 |
| **R-13** | Chưa ánh xạ thành viên–tài khoản hoặc deadline | Medium | Quyền sở hữu và escalation không rõ | Project Lead | Hoàn thiện roster với GitHub handle và ngày mục tiêu | Project Lead |
| **R-14** | Nhánh đã merge còn tồn tại; dọn nhánh thủ công | Low | Rối nhánh và nhầm lẫn | Project Lead | Xóa nhánh đã merge sau khi xác nhận không còn việc | Project Lead |
| **R-15** | CI xanh nhưng kiểm tra nông có thể che code hỏng | Medium | Tín hiệu sẵn sàng sai | TV6 | Thêm test, kiểm tra schema và smoke có assertion | TV6 |

Thang mức độ: **Critical** chặn toàn bộ tích hợp; **High** chặn một module hoặc cổng nghiệm thu; **Medium** gây làm lại hoặc đảm bảo yếu; **Low** là vệ sinh.

---

## 6. Minh chứng kiểm chứng và hạn chế

### Minh chứng thu thập ngày 2026-11-11

| Kiểm tra | Kết quả |
| :--- | :--- |
| GitHub Issues | 0 |
| GitHub Milestones | 0 |
| Pull Requests | 13 tổng: #1, #2, #4, #5, #6, #7, #9, #10, #11, #12, #13 đã merge; #3, #8 đã đóng |
| Nhánh chính | `main` tại `f7f5862` |
| CI | Hai job: `repository-hygiene` và `tv2-datasets` |
| Test tự động | `python -m unittest discover -s tests`: **60 test pass** |
| Kiểm tra fixture | `python scripts/validate_dataset.py data/samples/`: **10 dataset hợp lệ, 0 lỗi** |
| Liên kết Markdown nội bộ | **0 liên kết hỏng** trên 33 file |
| Module mã nguồn | `src/` chỉ có README tạm; `tests/` có bộ TV2; `scripts/` có prototype cũ và công cụ TV2 |
| Dependency manifest | `pyproject.toml` (đóng gói, extra `data`/`dev`, cấu hình pytest/ruff) |
| Smoke `scripts/validate_orders.py` | Đã chạy; xử lý 3 kho và 2 đơn; in phân bổ |
| Cú pháp JSON | Fixture trong `data/samples/` và `data/legacy/` đều parse được |

### Hạn chế

- Báo cáo dùng nội dung `main` đã commit; các thay đổi chưa commit trong working tree (bao gồm đợt Việt hóa này) chưa được tính.
- Không truy cập được trao đổi nội bộ, deadline bên ngoài hoặc công việc ngoài repository.
- Không có minh chứng test nào ngoài bộ TV2 và kiểm tra vệ sinh CI.
- GitHub Projects chưa được dùng; không có dữ liệu milestone/issue để đối chiếu.
- `docs/reference/project-analysis.docx` được coi là hạng mục bàn giao hộp đen; nội dung không được dùng làm minh chứng đã kiểm chứng.

---

## 7. Tài liệu liên quan

- [Theo dõi nhiệm vụ](task-tracker.md)
- [Kế hoạch tích hợp](integration-plan.md)
- [Kế hoạch kiểm thử](test-plan.md)
- [Phân công thành viên](../team-responsibilities.md)
- [Hướng dẫn tích hợp](../integration-guide.md)
- [Chiến lược kiểm thử](../testing-strategy.md)
