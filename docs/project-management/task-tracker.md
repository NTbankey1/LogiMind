# Theo dõi nhiệm vụ LogiMind

> **Chủ sở hữu:** Project Lead / TV6
> **Kiểm chứng lần cuối:** 2026-11-11
> **Nguồn trạng thái:** artifact trong repository, commit, PR và CI trên `main` tại `f7f5862`.
> **Quy tắc phân công:** tài liệu này ghi lại trách nhiệm đã có trong [Phân công thành viên](../team-responsibilities.md). Tài liệu **không** thay đổi phân công. Tên, GitHub handle và deadline vẫn là `TBD` cho đến khi nhóm xác nhận.

---

## 1. Trách nhiệm hiện có của nhóm

Phạm vi dưới đây lấy từ [docs/team-responsibilities.md](../team-responsibilities.md). Tài liệu nguồn ghi mọi vai trò là "Đang lập kế hoạch" và mọi người phụ trách là `TBD`.

| Vai trò | Trách nhiệm | Hạng mục bàn giao chính đã ghi | Phụ thuộc đã ghi | Danh tính |
| :--- | :--- | :--- | :--- | :--- |
| **TV1** | Phân tích nghiệp vụ và mô hình toán học | `docs/mathematical-model.md`; quy tắc nghiệp vụ trong `docs/requirements.md`; tính tay bài toán nhỏ; quyết định Policy A | Không (khởi tạo mô hình) | Tên / handle / deadline: `TBD` |
| **TV2** | Dữ liệu và bộ dữ liệu kiểm thử | `docs/data-dictionary.md`; fixture trong `data/samples/`; generator và validator schema trong `scripts/` | Định nghĩa tham số của TV1 | Tên / handle / deadline: `TBD` |
| **TV3** | Thuật toán tối ưu | Cài đặt baseline và MILP trong `src/logimind/algorithms/`; adapter bộ giải; so sánh benchmark; unit test | Mô hình TV1; bộ dữ liệu TV2 | Tên / handle / deadline: `TBD` |
| **TV4** | Frontend | Ứng dụng UI trong `frontend/`; dashboard phân bổ; hiển thị công suất/chi phí; phản hồi lỗi | API và mock response của TV5 | Tên / handle / deadline: `TBD` |
| **TV5** | Backend và cơ sở dữ liệu | Ứng dụng FastAPI trong `src/logimind/backend/`; model/migration SQLite; endpoint API; kiểm tra dữ liệu và timeout | Adapter TV3; schema TV2 | Tên / handle / deadline: `TBD` |
| **TV6** | Tích hợp, kiểm thử, báo cáo | Bộ test trong `tests/`; cổng chất lượng CI; integration test; báo cáo benchmark; báo cáo và demo cuối kỳ | Hạng mục bàn giao TV1–TV5 | Tên / handle / deadline: `TBD` |

> GitHub hiện có **0 Issue và 0 milestone**; tài liệu này là phương án thay thế dựa trên repository cho đến khi Project Lead tạo issue chính thức. Đây không phải cơ chế phân công.

---

## 2. Theo dõi workstream

Từ vựng trạng thái: **Completed**, **In Progress**, **Blocked**, **Not Started**, **Unable to Verify**.
"Minh chứng" là artifact trong repository hoặc bản ghi GitHub, không phải ước lượng nỗ lực.

### TV1 — Yêu cầu nghiệp vụ và mô hình toán học

| ID | Hạng mục bàn giao | Tiêu chí nghiệm thu | Trạng thái | Phụ thuộc | Minh chứng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV1-01 | Xác nhận quyết định chính sách (đã chọn Policy A) và ngữ nghĩa tham số | Quyết định Policy A được ghi và xác nhận; `C_j`, `c_ij` và các câu hỏi lưu trữ/phạm vi còn lại rõ ràng | **Blocked** | Nhóm phê duyệt; ảnh hưởng dữ liệu TV2 | [model §3–§4](../mathematical-model.md); [requirements §3](../requirements.md); [ADR-004](../decisions/0004-allocation-policy-a.md) |
| TV1-02 | Baseline yêu cầu FR01–FR08 và T1–T9 | Yêu cầu được review, không mơ hồ và truy vết được tới mã test | **In Progress** | TV1-01 | [requirements §5–§7](../requirements.md) |
| TV1-03 | Bàn giao mô hình cho TV2/TV3 kèm kiểm chứng ví dụ | Ví dụ tính tay được tái lập; minh chứng checklist bàn giao được đính kèm; giả định mô hình được sign-off | **Blocked** | TV1-01; schema TV2 | [model §6–§9](../mathematical-model.md); [integration-guide §3.1](../integration-guide.md) |

### TV2 — Dữ liệu và bộ dữ liệu kiểm thử

| ID | Hạng mục bàn giao | Tiêu chí nghiệm thu | Trạng thái | Phụ thuộc | Minh chứng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV2-01 | Schema dữ liệu chuẩn | Một schema Policy A bao phủ kho, tồn kho theo SKU, đơn hàng, công suất theo số đơn và chi phí vận chuyển; tên trường/kiểu/đơn vị được ghi | **Completed** | TV1-01 (chọn chính sách) | [schema](../../data/schema/dataset.schema.json); [data dictionary](../data-dictionary.md); [ADR-004](../decisions/0004-allocation-policy-a.md) |
| TV2-02 | Fixture benchmark | Fixture nhỏ/vừa/lớn khả thi, ít nhất một fixture chắc chắn không khả thi và sáu edge case được ghi; tất cả pass kiểm tra schema | **Completed** | TV2-01 | Mười fixture trong `data/samples/`; danh mục tại [data/README.md](../../data/README.md) |
| TV2-03 | Generator và validator bộ dữ liệu | Script chạy được, kiểm tra schema và bất biến, từ chối fixture sai với lỗi rõ ràng và sinh bộ dữ liệu khả thi tái lập được | **Completed** | TV2-01 | [scripts/README.md](../../scripts/README.md); [tests/test_datasets.py](../../tests/test_datasets.py) |
| TV2-04 | Đồng bộ tài liệu dữ liệu | Một từ điển chính thức; README/mô tả mẫu khớp fixture thực tế | **Completed** | TV2-01 | [data dictionary](../data-dictionary.md); bản trùng ở thư mục gốc đã gộp thành Phụ lục A; [README](../../README.md) |

### TV3 — Thuật toán tối ưu

| ID | Hạng mục bàn giao | Tiêu chí nghiệm thu | Trạng thái | Phụ thuộc | Minh chứng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV3-01 | Cài đặt heuristic baseline | Cài đặt đúng quy tắc thứ tự/phá hòa đã ghi; dùng đầu vào chuẩn; trả phân bổ và chỉ số | **Not Started** | TV1-01, TV2-01 | [model §5](../mathematical-model.md); `src/` chỉ có README |
| TV3-02 | Cài đặt MILP | Cài đặt đúng chính sách đã duyệt; tôn trọng ràng buộc tồn kho và công suất; báo trạng thái và thành phần mục tiêu | **Not Started** | TV1-01, TV2-01, TV3-01 | [model §3](../mathematical-model.md) |
| TV3-03 | Adapter bộ giải | Hợp đồng callable ổn định theo hướng dẫn tích hợp; đầu vào/đầu ra tất định; hành vi lỗi và timeout | **Not Started** | TV3-01, TV3-02 | [integration-guide §3.3](../integration-guide.md) |
| TV3-04 | Test thuật toán và báo cáo benchmark | Unit test bao phủ bất biến và edge case; chi phí MILP không tệ hơn baseline trên fixture chuẩn; thời gian/trạng thái được ghi | **Not Started** | TV3-01–TV3-03; harness TV6 | [testing-strategy](../testing-strategy.md); bộ TV2 đã có, test TV3 còn chờ |

### TV4 — Frontend

| ID | Hạng mục bàn giao | Tiêu chí nghiệm thu | Trạng thái | Phụ thuộc | Minh chứng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV4-01 | Khung ứng dụng frontend | Ứng dụng khởi động bằng lệnh được ghi; chế độ mock không cần backend | **Not Started** | Hợp đồng API TV5 | Không có file frontend hoặc manifest; [integration-guide §3.4](../integration-guide.md) |
| TV4-02 | Dashboard phân bổ | Người dùng chọn/tải bộ dữ liệu, chạy phân bổ và xem phân bổ, chi phí, mức sử dụng và lỗi | **Not Started** | TV4-01, API TV5 | [requirements FR01–FR07](../requirements.md) |
| TV4-03 | Tích hợp API | UI dùng hợp đồng API đã duyệt và xử lý lỗi kiểm tra, không khả thi, timeout và không có phương án | **Not Started** | TV4-02, cài đặt TV5, sign-off TV1/TV5 | [api-contract](../api-contract.md) đã căn chỉnh Policy A; cài đặt TV5 còn chờ |
| TV4-04 | Minh chứng sẵn sàng E2E | Luồng UI được ghi có thể chạy với backend thật cho E2E của TV6 | **Not Started** | TV4-03, cài đặt TV5 | [integration-guide §3.4](../integration-guide.md) |

*Policy A đã được quyết định: TV4 phải hiển thị đúng một kho cho mỗi đơn và không có giao diện split/penalty.*

### TV5 — Backend và cơ sở dữ liệu

| ID | Hạng mục bàn giao | Tiêu chí nghiệm thu | Trạng thái | Phụ thuộc | Minh chứng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV5-01 | Cài đặt API | Endpoint khớp hợp đồng API đã duyệt, gồm envelope, kiểm tra và ngữ nghĩa lỗi | **Not Started** | TV1-01, TV2-01, TV3-03 | [api-contract](../api-contract.md) đã căn chỉnh Policy A; chưa có cài đặt |
| TV5-02 | Lưu trữ SQLite | Schema/model và migration lưu lần chạy, phân bổ, cấu hình, chỉ số; file database không bao giờ được commit | **Not Started** | TV2-01, TV5-01 | ADR-003 vẫn `PROPOSED`; `.gitignore` đã bỏ qua `*.db`, `*.sqlite`, `*.sqlite3` |
| TV5-03 | Tích hợp bộ giải và timeout | Backend gọi adapter bộ giải với timeout cấu hình được và trả trạng thái/lỗi đã ghi | **Not Started** | TV3-03, TV5-01 | [integration-guide §3.5](../integration-guide.md) |
| TV5-04 | Test backend | Contract test và integration test pass trên SQLite và fixture | **Not Started** | TV5-01–TV5-03; harness TV6 | Bộ TV2 đã có, test TV5 còn chờ |

### TV6 — Tích hợp, kiểm thử, báo cáo

| ID | Hạng mục bàn giao | Tiêu chí nghiệm thu | Trạng thái | Phụ thuộc | Minh chứng |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TV6-01 | Bộ tài liệu quản lý dự án | Trạng thái, tracker, kế hoạch tích hợp và kế hoạch test tồn tại và khớp minh chứng repository | **In Progress** | Không | Tài liệu này; [project-status](project-status.md); [integration-plan](integration-plan.md); [test-plan](test-plan.md) |
| TV6-02 | Truy vết yêu cầu và kế hoạch test | T1–T9 và EDGE-01–10 được ánh xạ tới mã test, bậc, điều kiện tiên quyết và minh chứng | **In Progress** | Baseline yêu cầu TV1 | [test-plan](test-plan.md) |
| TV6-03 | Bộ kiểm thử | Cấu trúc `pytest`, fixture và helper tồn tại; test chạy được cục bộ và trong CI | **In Progress** | TV1-01, TV2-01 | `tests/test_datasets.py` (60 test) đã có; harness mở rộng còn chờ |
| TV6-04 | Job CI kiểm thử | CI cài dependency và chạy bộ test; lỗi chặn merge | **In Progress** | TV6-03; cập nhật ruleset của Project Lead | [ci.yml](../../.github/workflows/ci.yml) chạy job TV2 dataset/test; required-status-check còn chờ |
| TV6-05 | Test hợp đồng, tích hợp và E2E | Test bao phủ adapter bộ giải, API, lưu trữ SQLite và luồng dataset → API → solver → DB → UI | **Not Started** | TV3-03, TV5-01–TV5-03, TV4-04 | [testing-strategy](../testing-strategy.md) |
| TV6-06 | Quy trình bug tracking và kiểm chứng | Bug có bước tái hiện, mức độ, mong đợi/thực tế và minh chứng đóng; mẫu issue được dùng | **Not Started** | Project Lead bật quy trình issue | `.github/ISSUE_TEMPLATE/` tồn tại; 0 issue được tạo |
| TV6-07 | Benchmark và báo cáo cuối kỳ | So sánh Baseline/MILP, tóm tắt test, hạn chế đã biết, kịch bản demo và báo cáo cuối kỳ được tạo từ minh chứng đã chạy | **Not Started** | Hạng mục TV1–TV5; TV6-05 | [team-responsibilities](../team-responsibilities.md) |

---

## 3. Tóm tắt phụ thuộc

```text
TV1-01 (quy tắc được duyệt)
  -> TV2-01 (schema chuẩn)
      -> TV2-02/03 (fixture + validator)
      -> TV3-01/02/03 (baseline, MILP, adapter)
          -> TV5-01/02/03 (API, SQLite, tích hợp bộ giải)
              -> TV4-01/02/03 (UI, dashboard, API thật)
                  -> TV6-05 (contract/integration/E2E)
                      -> TV6-07 (benchmark + báo cáo cuối kỳ)
TV6-02/03/04 (truy vết, harness, job CI) có thể bắt đầu trước khi TV3–TV5 hoàn tất.
```

---

## 4. Quy tắc minh chứng trạng thái

- Một nhiệm vụ chỉ chuyển **Completed** khi tiêu chí nghiệm thu được chứng minh bằng artifact đã commit, output test đã chạy hoặc PR đã merge.
- Một nhiệm vụ là **Blocked** khi phụ thuộc chưa được giải quyết rõ ràng; blocker được ghi tại [project-status §4](project-status.md#4-blocker-và-phụ-thuộc).
- Một nhiệm vụ là **In Progress** chỉ khi artifact tồn tại trong repository, không phải khi mới được lập kế hoạch hoặc thảo luận.
- Cập nhật ngày kiểm chứng và liên kết minh chứng mỗi khi trạng thái thay đổi.
- Tài liệu này không thay thế GitHub Issues. Khi Project Lead tạo issue/milestone chính thức, hãy liên kết tại đây thay vì sao chép trạng thái.

---

## 5. Thông tin còn thiếu cần nhóm xác nhận

1. Tài khoản GitHub của từng vai trò TV.
2. Nhóm xác nhận Policy A do Project Lead chọn trong [ADR-004](../decisions/0004-allocation-policy-a.md), và các xung đột quy tắc nghiệp vụ còn lại trong project-status §4.
3. Việc TV3/TV5/TV6 áp dụng schema Policy A chuẩn; schema và từ điển TV2 đã công bố nhưng các module chưa cập nhật.
4. Sign-off của TV3/TV4/TV5 cho hợp đồng API Policy A và ngữ nghĩa trạng thái.
5. Ngày sprint và định nghĩa milestone.
6. Quyền sở hữu prototype cũ (`scripts/validate_orders.py`) và các bộ dữ liệu (`data/samples/`, `data/legacy/`).
