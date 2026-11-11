# Kế hoạch kiểm thử LogiMind

> **Chủ sở hữu:** TV6 (Tích hợp, Kiểm thử & Báo cáo)
> **Kiểm chứng lần cuối:** 2026-11-11
> **Baseline:** `main` tại `f7f5862`
> **Nguyên tắc:** Không báo một test là pass nếu chưa thực sự chạy và quan sát output. Test dự kiến được đánh dấu là dự kiến, không phải đã hoàn thành.

---

## 1. Mục tiêu và phạm vi

Kế hoạch này định nghĩa cách TV6 kiểm chứng LogiMind đáp ứng yêu cầu trong [requirements.md](../requirements.md) và các bất biến/edge case trong [testing-strategy.md](../testing-strategy.md). Phạm vi gồm unit, contract, integration, system và end-to-end test. Tài liệu **không** định nghĩa lại quy tắc nghiệp vụ, schema API hoặc thuật toán thuộc TV1–TV5.

**Trong phạm vi:** hành vi phân bổ, bất biến toán học, kiểm tra dữ liệu, hợp đồng API, lưu trữ, tích hợp bộ giải, luồng UI và minh chứng báo cáo.
**Ngoài phạm vi:** tinh chỉnh hiệu năng ngoài các chỉ số benchmark đã ghi, triển khai production và các quyết định quy tắc nghiệp vụ chưa được duyệt.

---

## 2. Hiện trạng kiểm thử

| Hạng mục | Trạng thái | Minh chứng |
| :--- | :--- | :--- |
| Bộ test tự động | **Đã triển khai (TV2)** | `tests/test_datasets.py`, 60 test; đã chạy pass ngày 2026-11-11 |
| Cấu hình framework test | **Đã có** | `pyproject.toml` có `[tool.pytest.ini_options]` |
| CI chạy test | **Đã có (job TV2)** | [.github/workflows/ci.yml](../../.github/workflows/ci.yml) chạy `python -m unittest discover -s tests -v` |
| Kiểm tra cú pháp JSON | **Có trong CI** | Fixture trong `data/samples/` và `data/legacy/` được parse bằng `python -m json.tool` |
| Kiểm tra liên kết Markdown | **Có trong CI** | Liên kết tương đối nội bộ được kiểm tra |
| Kiểm tra file thiết yếu | **Có trong CI** | README, CLAUDE, CONTRIBUTING, CHANGELOG, `.gitignore`, `.editorconfig`, `.gitattributes` |
| Smoke prototype | **Có trong CI (không assertion)** | `python scripts/validate_orders.py` |
| Test theo yêu cầu (T1–T9) | **Chưa triển khai** | Bảng yêu cầu tồn tại, chưa có mã test tương ứng |
| Test edge case (EDGE-01–10) | **Một phần** | Bộ TV2 kiểm chứng trạng thái khả thi của fixture ở mức dữ liệu; chưa có test bộ giải/API cho từng EDGE |
| Test API/DB/frontend/solver | **Chưa thể thực hiện** | Các module chưa tồn tại |

**Kết luận:** CI đã chạy bộ test dữ liệu TV2, nhưng chưa chứng minh tính đúng đắn của phân bổ, thỏa mãn ràng buộc ở mức bộ giải hoặc hành vi tích hợp.

---

## 3. Các bậc kiểm thử và trách nhiệm

| Bậc | Mục đích | Người thực hiện | Điều kiện tiên quyết | Minh chứng chính |
| :--- | :--- | :--- | :--- | :--- |
| **Unit** | Kiểm tra hàm, validator, heuristic và tính chi phí độc lập | Chủ sở hữu module (TV3/TV5); TV6 review minh chứng | Mã module; fixture chuẩn | Lệnh test, output pass/fail, báo cáo coverage nếu có |
| **Contract** | Kiểm tra adapter bộ giải và ranh giới API theo hợp đồng đã chốt | TV6 cùng TV3/TV5 | Hợp đồng G1; cài đặt adapter/API | Output contract test; bản ghi request/response |
| **Integration** | Kiểm tra API ↔ solver ↔ SQLite trên fixture chuẩn | TV6 cùng TV5 | Fixture G2; bộ giải G3; backend G4 | Log lần chạy tích hợp; minh chứng đọc lại DB |
| **System** | Kiểm tra hành vi backend end-to-end, gồm lỗi/không khả thi/timeout | TV6 | Backend G4; fixture G2 | Báo cáo system test; minh chứng trạng thái/HTTP |
| **E2E** | Kiểm tra luồng người dùng từ chọn dữ liệu đến hiển thị kết quả | TV6 cùng TV4 | Frontend G5; backend thật | Bản ghi walkthrough; output E2E test |
| **Benchmark/hiệu năng** | Ghi chi phí Baseline và MILP, thời gian, trạng thái và mức sử dụng | TV3 cung cấp; TV6 kiểm chứng | Bộ giải G3; fixture G2 | Bảng benchmark kèm môi trường và cấu hình chạy |

Các bậc trong [testing-strategy.md §3](../testing-strategy.md) vẫn là tham chiếu chính. Công cụ nêu ở đó (`pytest`, Playwright/request test tùy chọn) là **đề xuất**; `pytest` đã có trong extra `dev`, các công cụ còn lại chưa cấu hình.

---

## 4. Truy vết yêu cầu — T1 đến T9

Nguồn: [requirements.md §7](../requirements.md) (T1–T9). "Có thể chuẩn bị ngay" nghĩa là thiết kế test/fixture có thể soạn mà không cần mã module; việc thực thi vẫn cần điều kiện tiên quyết.

| Mã test | Yêu cầu | Nguồn | Bậc | Module kiểm thử | Chuẩn bị ngay? | Điều kiện tiên quyết | Minh chứng mong đợi | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T1** | Ví dụ nhỏ tính tay khớp chi phí và phân bổ hợp lệ, hoặc được kiểm chứng vét cạn | requirements T1 | Unit + System | Bộ giải TV3 / checker độc lập | Chỉ thiết kế test | Mô hình đã duyệt; bộ giải; fixture chuẩn | Mục tiêu và phân bổ tái lập so với tính tay | **Blocked** |
| **T2** | Đủ tồn kho và công suất; mọi đơn được gán | requirements T2 | Unit + Integration | Bộ giải (Policy A) | Chỉ thiết kế test | Bộ giải; fixture chuẩn | Mọi đơn gán cho một kho; mục tiêu khớp chi phí vận chuyển | **Blocked** |
| **T3** | Kho rẻ nhất thiếu một SKU không được nhận cả đơn | requirements T3 | Unit | Baseline/MILP | Chỉ thiết kế test | Bộ giải; tồn kho theo SKU | Phân bổ tránh kho không hợp lệ; kiểm tra bất biến | **Blocked** |
| **T4** | Kho rẻ nhất hết công suất không bị vượt; dùng kho khác | requirements T4 | Unit + Integration | Ràng buộc công suất của bộ giải | Chỉ thiết kế test | Ngữ nghĩa công suất; bộ giải | Mức sử dụng ≤ `capacity_orders`; đơn được gán cho kho khác đủ điều kiện | **Blocked** |
| **T5** | Tồn kho và công suất cùng căng được tôn trọng | requirements T5 | Unit + Invariant | Bộ giải | Chỉ thiết kế test | Bộ giải; validator | Mọi bất biến tồn kho/công suất đúng | **Blocked** |
| **T6** | Không thể giao đủ đơn được báo đúng | requirements T6 | Unit + System | Bộ giải + trạng thái API | Chỉ thiết kế test | Bộ giải; API; hợp đồng trạng thái | `INFEASIBLE` chỉ khi có chứng minh; `NO_SOLUTION_FOUND` khi timeout không chứng minh | **Blocked** |
| **T7** | Dữ liệu lỗi bị từ chối với đúng mã/trường; dừng thực thi | requirements T7 | Unit + Contract | Validator dữ liệu/API | **Có**, thiết kế test | Schema chuẩn; cài đặt kiểm tra | Payload lỗi kiểm tra; không chạy bộ giải | **Blocked** |
| **T8** | Chi phí bằng nhau phá hòa theo mã kho; MILP có thể có nhiều tối ưu | requirements T8 | Unit | Baseline/MILP | Chỉ thiết kế test | Bộ giải; quy tắc phá hòa | Kết quả baseline tất định; các tối ưu MILP hợp lệ | **Blocked** |
| **T9** | Quy mô lớn ghi thời gian, trạng thái và chất lượng lời giải trong giới hạn thời gian | requirements T9 | Performance/System | Bộ giải/API | Chỉ thiết kế test | Bộ giải; fixture quy mô; cấu hình timeout | Thời gian chạy, trạng thái (gồm `FEASIBLE`/`NO_SOLUTION_FOUND`), mục tiêu/gap, môi trường | **Blocked** |

---

## 5. Ánh xạ edge case — EDGE-01 đến EDGE-10

Nguồn: [testing-strategy.md §4](../testing-strategy.md).

| Mã test | Edge case | Hành vi mong đợi | Bậc | Chuẩn bị ngay? | Điều kiện tiên quyết | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EDGE-01** | Hết hàng toàn hệ thống: cầu một SKU vượt tổng tồn kho | `INFEASIBLE` kèm chứng minh; `NO_SOLUTION_FOUND` nếu tìm kiếm dừng mà chưa chứng minh | System + Invariant | Chỉ thiết kế dữ liệu test | Bộ giải; tồn kho chuẩn; hợp đồng trạng thái | **Blocked** |
| **EDGE-02** | Nghẽn kho: kho gần nhất còn hàng nhưng hết công suất | Chuyển sang kho khác còn công suất | Unit + Integration | Chỉ thiết kế dữ liệu test | Bộ giải; fixture công suất | **Blocked** |
| **EDGE-03** | Công suất và tồn kho cùng căng: chỉ một phương án đầy đủ cụ thể hoạt động | Bộ giải tìm ra phương án hoặc chứng minh `INFEASIBLE`; không tách đơn/bỏ đơn | Unit + System | Chỉ thiết kế dữ liệu test | Bộ giải; fixture căng (`edge_tight_capacity`, `edge_tight_inventory`) | **Blocked** |
| **EDGE-04** | Đơn nhu cầu bằng 0 | Kiểm tra đầu vào từ chối với lỗi đã ghi (testing-strategy dùng HTTP 400) | Contract | **Có**, thiết kế test | Kiểm tra API/schema | **Blocked** |
| **EDGE-05** | Chi phí/công suất bằng nhau | Phân bổ tất định qua các lần chạy lặp lại | Unit | Chỉ thiết kế test | Bộ giải; quy tắc phá hòa | **Blocked** |
| **EDGE-06** | Một tuyến bị bỏ khỏi `shipping_costs` | Kho bị bỏ không bao giờ được dùng | Unit + Invariant | Chỉ thiết kế dữ liệu test | Bộ giải; fixture chuẩn | **Blocked** |
| **EDGE-07** | Chỉ một kho có tuyến và đủ tồn kho/công suất | Đơn buộc gán cho kho đó | Unit + Integration | Chỉ thiết kế dữ liệu test | Bộ giải; fixture chuẩn | **Blocked** |
| **EDGE-08** | Hết thời gian mà chưa có phương án đầy đủ | `NO_SOLUTION_FOUND`, không phải `INFEASIBLE` | System | Chỉ thiết kế test | Bộ giải; cấu hình timeout | **Blocked** |
| **EDGE-09** | Hết thời gian sau khi đã có phương án đầy đủ | `FEASIBLE` với phân bổ đầy đủ | System | Chỉ thiết kế test | Bộ giải; cấu hình timeout | **Blocked** |
| **EDGE-10** | Bộ dữ liệu hợp lệ về cấu trúc nhưng không khả thi về toán học | `INFEASIBLE` kèm chứng minh; bộ dữ liệu vẫn hợp lệ | System + Contract | **Có**, thiết kế dữ liệu test | Fixture chuẩn; bộ giải/checker | **Blocked** |

> Policy A đã được quyết định tại [ADR-004](../decisions/0004-allocation-policy-a.md); test giao tách đơn và penalty không thuộc chiến lược hiện hành.

---

## 6. Yêu cầu dữ liệu kiểm thử

| Yêu cầu | Dữ liệu cần | Hiện trạng |
| :--- | :--- | :--- |
| Schema đầu vào chuẩn | Kho, tồn kho theo SKU, đơn hàng, dòng đơn, chi phí vận chuyển | TV2 đã triển khai: `data/schema/dataset.schema.json` + `docs/data-dictionary.md` |
| Ca nhỏ tính tay được | Khớp T1/ví dụ mô hình | `data/samples/sample_small.json` (2 kho/3 đơn/2 SKU); xem được bằng tay nhưng không trùng số liệu với ví dụ trong mô hình |
| Ca khả thi | Đủ tồn kho và công suất | Đã bao phủ bởi fixture chuẩn TV2; fixture prototype là non-Policy-A |
| Ca không khả thi | Cầu vượt nguồn lực | `sample_infeasible.json`, `edge_infeasible_stock.json` |
| Ca tài nguyên căng | T5 | `edge_tight_capacity.json`, `edge_tight_inventory.json` |
| Ca phá hòa | T8 | `edge_equal_costs.json` |
| Ca quy mô | T9 | Chưa xác định |
| Ca dữ liệu lỗi | T7 | Chưa triển khai thành fixture |

TV2 sở hữu sinh dữ liệu và kiểm tra schema. TV6 sẽ kiểm chứng độc lập fixture theo schema đã duyệt; TV6 không tự tạo dữ liệu nghiệp vụ chuẩn trừ khi nhóm giao việc.

---

## 7. Điều kiện tiên quyết

### 7.1. Bắt buộc trước mọi test nghiệm thu

- Quy tắc nghiệp vụ được duyệt và một schema dữ liệu chuẩn duy nhất (G0).
- Hợp đồng `ProblemInput`/`SolutionOutput` và hợp đồng API đã chốt (G1).
- Fixture đã kiểm tra bao phủ T1–T9 và EDGE-01–10 (G2).
- Module bộ giải/API có lệnh khởi động được ghi (G3/G4).
- Dependency manifest và môi trường tái lập được.
- Định dạng minh chứng test được thống nhất: lệnh, commit SHA, môi trường, output quan sát.

### 7.2. Đã có

- Môi trường Python 3.10+ (CI dùng 3.10).
- Bộ test TV2 (60 test) và job CI dataset/feasibility.
- Kiểm tra vệ sinh repository trong CI.
- Fixture JSON cho kiểm tra cú pháp và kiểm chứng khả thi.
- Bảng yêu cầu/edge case để sinh mã test.

### 7.3. Chưa có

- Fixture cho test quy mô (T9) và dữ liệu lỗi (T7).
- Bộ giải, API, cơ sở dữ liệu và frontend.
- Mock API/server cho contract test sớm.
- Bộ test TV3/TV5/TV4.

---

## 8. Minh chứng và tiêu chí nghiệm thu

### 8.1. Minh chứng cho mỗi test

Mọi test đã chạy phải ghi:

1. Mã test và liên kết yêu cầu/edge case.
2. Lệnh và môi trường.
3. Commit SHA hoặc tham chiếu PR.
4. Output quan sát (pass/fail, trạng thái, mục tiêu, bất biến).
5. Với lỗi: mong đợi so với thực tế, bước tái hiện, issue bug liên kết.
6. Với benchmark: phiên bản bộ dữ liệu, thuật toán, giới hạn thời gian, thời gian chạy, trạng thái, thành phần chi phí, mức sử dụng.

### 8.2. Điều kiện vào nghiệm thu

- Minh chứng thoát G0–G4 tồn tại.
- Dữ liệu test được kiểm tra và đánh phiên bản.
- Không còn xung đột quy tắc nghiệp vụ P0 đã biết.
- CI chạy được bộ test.

### 8.3. Điều kiện ra nghiệm thu cuối kỳ

- **T1–T9:** tất cả được thực thi với minh chứng đã ghi; mọi ngoại lệ được ghi rõ và phê duyệt.
- **EDGE-01–10:** tất cả được thực thi, hoặc hoãn rõ ràng với lý do được duyệt theo [testing-strategy.md §4](../testing-strategy.md).
- **Bất biến:** đúng một kho cho mỗi đơn, không tách/không bỏ đơn, không vi phạm tồn kho hoặc công suất.
- **API:** hợp đồng, kiểm tra, không khả thi và timeout khớp hợp đồng đã duyệt.
- **Lưu trữ:** lần chạy đã lưu đọc lại với cấu hình và chỉ số giống hệt.
- **E2E:** chọn dữ liệu → giải → kết quả được minh chứng trên stack thật.
- **Tái lập:** cùng đầu vào/cấu hình cho kết quả so sánh được như đã ghi.
- **Báo cáo:** benchmark và báo cáo cuối kỳ trích dẫn minh chứng đã chạy, không phải việc dự kiến.

Không đặt mục tiêu coverage số học vì repository không định nghĩa; coverage có thể báo cáo như minh chứng bổ sung, không thay thế việc thực thi T1–T9/EDGE.

---

## 9. Có thể chuẩn bị ngay và phải chờ

### 9.1. Có thể chuẩn bị ngay (TV6 sở hữu)

- Duy trì ma trận truy vết (tài liệu này).
- Mô tả chi tiết test case cho T1–T9 và EDGE-01–10, gồm kết quả mong đợi từ yêu cầu hiện có.
- Thiết kế test dữ liệu lỗi cho T7/EDGE-04.
- Thiết kế job CI test (lệnh pytest, thu thập artifact/báo cáo).
- Quy trình báo lỗi và kiểm chứng dùng mẫu issue hiện có.
- Checklist review fixture cho TV2 (tuân thủ schema, kết quả mong đợi, phiên bản).
- Mẫu minh chứng và khung báo cáo nghiệm thu.
- Kiểm tra vệ sinh repository (cú pháp JSON, liên kết, hành vi `.gitignore`).

### 9.2. Phải chờ module khác

- Unit test cho baseline/MILP (TV3).
- Contract test cho adapter bộ giải (TV3) và API (TV5).
- Integration test cho lưu trữ SQLite (TV5).
- System test cho hành vi không khả thi/timeout (TV3/TV5).
- E2E test (TV4/TV5).
- Chạy benchmark/hiệu năng (TV3/TV5).

### 9.3. Cần phối hợp

- Enum trạng thái và ánh xạ lỗi giữa mô hình, bộ giải và API.
- Định dạng fixture chuẩn và định nghĩa edge case với TV2.
- Mock API cho TV4 trước khi backend hoàn tất.
- Định nghĩa minh chứng "done" cho từng handoff trong [integration-guide](../integration-guide.md).
- TV3/TV4/TV5 cài đặt hợp đồng API Policy A.

---

## 10. Bug tracking và kiểm chứng

Repository có mẫu issue nhưng chưa có issue. Cho đến khi Project Lead thiết lập quy trình issue, TV6 ghi lỗi trong báo cáo test với:

- Mã test và liên kết yêu cầu.
- Mức độ: Critical (chặn nghiệm thu), High (chặn module/cổng), Medium (làm lại), Low (vệ sinh).
- Bước tái hiện, mong đợi so với thực tế, môi trường.
- Minh chứng sau khi sửa và người review xác nhận.

Bug chỉ được đóng khi bản sửa được kiểm chứng bằng cách chạy lại test lỗi hoặc kiểm tra tái lập tương đương.

---

## 11. Duy trì truy vết

- Cập nhật ma trận mỗi khi TV1 thay đổi yêu cầu hoặc một quy tắc nghiệp vụ được duyệt.
- Liên kết mỗi mã test tới file và tên test khi bộ test tồn tại.
- Không đánh dấu test pass chỉ dựa trên review code.
- Nếu yêu cầu bị bỏ hoặc thay đổi, đánh dấu các mã test liên quan là retired và ghi lý do.

---

## 12. Tài liệu liên quan

- [Trạng thái dự án](project-status.md)
- [Theo dõi nhiệm vụ](task-tracker.md)
- [Kế hoạch tích hợp](integration-plan.md)
- [Yêu cầu hệ thống](../requirements.md)
- [Chiến lược kiểm thử](../testing-strategy.md)
- [Hướng dẫn tích hợp](../integration-guide.md)
