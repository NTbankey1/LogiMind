# Yêu cầu hệ thống LogiMind

LogiMind hỗ trợ phân bổ toàn bộ đơn hàng trong một đợt cho 2–3 kho, có xét tồn kho từng mặt hàng và công suất xử lý. Phiên bản này áp dụng **Policy A: mỗi đơn bắt buộc được giao nguyên vẹn từ đúng một kho**. Trong các phương án đáp ứng đủ đơn, hệ thống tìm phương án có tổng chi phí giao hàng thấp nhất.

Công thức và ví dụ bàn giao nằm trong [Mô hình toán học](mathematical-model.md). Một phương án chỉ phân bổ được một phần số đơn không được coi là kết quả hợp lệ của Policy A.

## 1. Người sử dụng và bài toán

Nhân viên điều phối nhập dữ liệu một đợt, chạy phân bổ và xem kho xử lý từng đơn. Quản lý kho theo dõi lượng hàng và công suất được sử dụng.

Chọn kho rẻ nhất cho từng đơn có thể chiếm hết nguồn lực mà các đơn sau cần. Hệ thống phải xét toàn bộ tập đơn, đồng thời giữ đúng giới hạn tồn kho và công suất.

## 2. Phạm vi và quy tắc nghiệp vụ

| Nội dung | Quy tắc áp dụng |
|---|---|
| Chính sách | A, bắt buộc giao đủ mọi đơn |
| Số kho | 2–3 kho trong một đợt |
| Đơn hàng | Có thể gồm nhiều mặt hàng; không tách một đơn giữa nhiều kho |
| Tồn kho | Cố định theo lượng khả dụng đầu đợt; không nhập thêm hoặc chuyển kho trong đợt |
| Công suất | Số đơn tối đa một kho xử lý; mỗi đơn chiếm 1 đơn vị |
| Chi phí | Ma trận chi phí giao nguyên đơn từ từng kho, cung cấp trước khi chạy |
| Khi không đủ nguồn lực | Không chấp nhận phương án thiếu đơn; chỉ báo không khả thi khi có chứng minh |
| Khi hết thời gian | Phân biệt có phương án đầy đủ và chưa tìm được phương án đầy đủ |

Dùng dữ liệu mô phỏng có seed cố định. Không tối ưu tuyến xe nhiều điểm, không dự báo nhu cầu và không tích hợp WMS/ERP hoặc dữ liệu thời gian thực. Chạy phân bổ là tạo kế hoạch đề xuất, không tự ghi nhận xuất hàng thực tế.

Mỗi thuật toán nhận bản sao của cùng dữ liệu gốc. Không dùng tồn kho đã bị Baseline trừ đi làm đầu vào cho MILP.

## 3. Cách tính chi phí vận chuyển

`shipping_cost[i,j]` là chi phí giao **toàn bộ đơn i** từ kho j, không phải đơn giá của một sản phẩm. Ví dụ đơn A cần 2 sản phẩm X và 1 sản phẩm Y, chi phí từ K2 là 14 nghìn đồng, thì giao A từ K2 tính 14, không tính `14 × 3`.

Tổng chi phí là tổng chi phí của từng đơn theo kho được chọn. Không cộng chi phí mở kho, không giảm giá do ghép đơn và không tính tuyến xe chung. Ma trận được nhập hoặc sinh sẵn có seed; bản tối thiểu không tính chi phí từ bản đồ, trọng lượng hoặc nhiên liệu.

Lưu `money_unit` cùng dữ liệu chạy và dùng một đơn vị cho toàn bộ ma trận và kết quả. Ví dụ kiểm chứng dùng nghìn đồng. Nếu quy đổi đơn vị tiền, phải thực hiện trước khi chạy và ghi lại cách quy đổi.

## 4. Dữ liệu đầu vào

Tên trường dưới đây là quy ước bàn giao đề xuất cho TV2, TV3 và TV5; cần đối chiếu khi tích hợp với mã nguồn.

| Dữ liệu | Trường | Ý nghĩa |
|---|---|---|
| Đơn hàng | `order_id` | Mã đơn duy nhất |
| Dòng hàng | `order_id`, `sku_id`, `quantity` | Nhu cầu từng mặt hàng của đơn |
| Kho | `warehouse_id`, `capacity` | Mã kho và số đơn tối đa trong đợt |
| Danh mục hàng | `sku_id` | Mã mặt hàng |
| Tồn kho | `warehouse_id`, `sku_id`, `stock` | Lượng khả dụng đầu đợt |
| Chi phí | `order_id`, `warehouse_id`, `shipping_cost` | Chi phí giao nguyên đơn từ kho |
| Cấu hình | `policy`, `money_unit`, `time_limit_seconds`, `seed` | `policy = A`, đơn vị tiền, thời gian tối đa và seed nếu sinh dữ liệu |

### Kiểm tra dữ liệu

1. Mã không trống và các mã tham chiếu phải tồn tại. Không nhận mã đơn trùng hoặc bản ghi trùng cặp kho–mặt hàng, đơn–mặt hàng, đơn–kho.
2. Mỗi đơn có ít nhất một dòng hàng; số lượng dòng hàng là số nguyên dương. Mặt hàng không xuất hiện trong đơn có nhu cầu bằng 0 trong mô hình.
3. Tồn kho và công suất là số nguyên không âm. Giá trị 0 hợp lệ, ô thiếu phải được báo lỗi.
4. Ma trận chi phí có giá trị hữu hạn không âm; không nhận NaN, vô cực hoặc số âm.
5. Bảng tồn phải ghi rõ mọi cặp kho–mặt hàng trong phạm vi dữ liệu; không có hàng phải ghi 0.
6. Cặp đơn–kho thiếu chi phí được loại khỏi lựa chọn và có cảnh báo. Không tự điền bằng 0. Quy tắc này giữ cách xử lý đã đề xuất trong bản TV1; cần thống nhất với bộ nạp dữ liệu khi tích hợp.
7. Nhu cầu vượt nguồn lực là tình huống không khả thi có thể kiểm chứng, không phải lỗi định dạng.
8. Tập đơn rỗng trả thông báo không có đơn để xử lý; không tính tỷ lệ bằng phép chia cho 0. Thực nghiệm đánh giá dùng ít nhất một đơn.

## 5. Yêu cầu chức năng

| Mã | Chức năng | Điều kiện nghiệm thu |
|---|---|---|
| FR01 | Nhập hoặc tải dữ liệu | Nhận đủ các bảng; chỉ rõ trường và mã bản ghi sai |
| FR02 | Xem dữ liệu trước khi chạy | Hiển thị số đơn, kho, tồn kho, công suất và cảnh báo thiếu chi phí |
| FR03 | Chạy Baseline | Xét đơn theo mã tăng dần, chọn kho còn đủ hàng và công suất có chi phí thấp nhất |
| FR04 | Chạy MILP | Dùng Policy A, đúng mô hình và giới hạn thời gian; trả trạng thái lời giải |
| FR05 | Kiểm tra độc lập | Kiểm tra đủ mọi đơn, một kho mỗi đơn, tồn kho, công suất và tổng chi phí |
| FR06 | Hiển thị kết quả | Chỉ đánh dấu phương án hợp lệ nếu giao đủ đơn và thỏa mọi ràng buộc |
| FR07 | So sánh | Cùng dữ liệu gốc, cùng Policy A; phân biệt trường hợp Baseline không tìm được phương án đầy đủ |
| FR08 | Lưu kết quả | Nếu lưu SQLite, lưu được đầu vào, cấu hình, phương án, trạng thái và chỉ số để đọc lại |

Xuất CSV/Excel, tách đơn, tải xử lý theo khối lượng và phí mở kho là phần mở rộng ngoài mô hình hiện tại.

## 6. Trạng thái và cách xử lý khi chưa có phương án

| Trạng thái | Ý nghĩa | Cách hiển thị |
|---|---|---|
| `OPTIMAL` | Có phương án đầy đủ và đã chứng minh chi phí tối ưu | Hiển thị phân bổ và chi phí |
| `FEASIBLE` | Có phương án đầy đủ, chưa chứng minh tối ưu | Hiển thị phương án hợp lệ tốt nhất tìm được |
| `INFEASIBLE` | Đã chứng minh không thể giao đủ đơn | Thông báo không khả thi; có thể kèm điều kiện chứng minh |
| `NO_SOLUTION_FOUND` | Bộ giải chưa tìm được phương án đầy đủ và chưa chứng minh vô nghiệm | Ghi rõ lý do dừng, không kết luận không khả thi |
| `BASELINE_FAILED` | Baseline tham lam không giao được hết đơn | Thông báo phương pháp chưa tìm được phương án đầy đủ, vẫn có thể chạy MILP |
| `ERROR` | Lỗi dữ liệu, dựng mô hình hoặc thực thi | Thông báo lỗi để kiểm tra |

Baseline chỉ có thể báo `FEASIBLE` hoặc `BASELINE_FAILED` khi thuật toán chạy bình thường; không tự chứng nhận tối ưu. Các gán đơn tạm thời khi Baseline thất bại chỉ dùng chẩn đoán, không phải phương án hoàn thành và không dùng chi phí phần này để so với lời giải đầy đủ của MILP.

Nếu không có phương án đầy đủ, `shipping_cost` và `objective_value` của kết quả chính để `null`, không gán 0. Chỉ bộ giải hoặc phép kiểm chứng độc lập có bằng chứng mới được kết luận `INFEASIBLE`.

Tổng tồn theo mặt hàng đủ và tổng công suất đủ chưa đảm bảo khả thi vì đơn không được tách và hàng phân tán giữa các kho. Hai điều kiện này chỉ dùng kiểm tra cần, không thay bộ giải.

## 7. Bộ kiểm thử và chỉ số

| Mã | Tình huống | Kết quả cần kiểm tra |
|---|---|---|
| T1 | Dữ liệu nhỏ tính tay | MILP khớp đáp án hoặc vét cạn khi xác nhận tối ưu |
| T2 | Có phương án giao toàn bộ | Kết quả hợp lệ phải chứa đủ mọi đơn |
| T3 | Kho rẻ nhất thiếu mặt hàng | Không gán đơn vào kho thiếu hàng |
| T4 | Kho rẻ nhất hết công suất | Dùng kho khác hoặc không tìm được phương án đầy đủ |
| T5 | Tồn và công suất cùng hạn chế | Đồng thời kiểm tra mọi ràng buộc |
| T6 | Nguồn lực không cho phép giao đủ | Báo `INFEASIBLE` nếu đã chứng minh; không trả phương án một phần như hợp lệ |
| T7 | Dữ liệu lỗi | Báo đúng mã, trường và không chạy dữ liệu chưa hợp lệ |
| T8 | Chi phí bằng nhau | Baseline phá hòa cố định; MILP được phép có nhiều nghiệm tối ưu |
| T9 | Quy mô tăng dần | Ghi thời gian, trạng thái, cận và gap nếu có |

Bổ sung tình huống Baseline thất bại nhưng MILP vẫn có nghiệm, và tình huống hết thời gian chưa tìm được nghiệm. Các ví dụ tương ứng nằm trong tài liệu mô hình.

Chỉ tính phần trăm giảm chi phí khi cả hai phương pháp có phương án đầy đủ hợp lệ và chi phí Baseline lớn hơn 0. Nếu Baseline thất bại, báo trạng thái và thời gian, không tính phần trăm tiết kiệm từ chi phí gán tạm thời.

Phương án hợp lệ của Policy A luôn phục vụ 100% đơn. Tỷ lệ này là điều kiện kiểm tra, không phải mục tiêu đánh đổi với chi phí. Theo dõi thêm tổng chi phí giao, mức sử dụng công suất mỗi kho, thời gian và tỷ lệ các lần chạy tìm được phương án hợp lệ. Không đưa đơn bị bỏ ra khỏi mẫu số để tăng tỷ lệ phục vụ.

## 8. Phân công và bàn giao

| Thành viên | Nội dung phối hợp |
|---|---|
| TV1 | Yêu cầu, giả định, mô hình, ví dụ tính tay và phân tích kết quả |
| TV2 | Cấu trúc dữ liệu, seed, bộ thử T1–T9 và vét cạn |
| TV3 | Baseline, MILP, trạng thái, thời gian và chi phí |
| TV4 | Giao diện dữ liệu, kết quả và tình huống không có phương án |
| TV5 | API, SQLite và lưu cấu hình chạy |
| TV6 | Kiểm tra độc lập, tích hợp và tổng hợp kết quả |

Trước khi tích hợp cần thống nhất cấu trúc trường, quy tắc thiếu chi phí, đơn vị tiền, bộ giải và giới hạn thời gian. Ghi phiên bản dữ liệu và môi trường chạy cùng kết quả. Chính sách của phiên bản tài liệu này là A.

## 9. Tài liệu nguồn

- [Tutorial Smart Logistics](https://docs.google.com/document/d/1ena1ZD8g8Emt3urDTUhlCquVawd5Pzar/edit), mục 3.1 và các mục 6–9.
- [Sheet Group8](https://docs.google.com/spreadsheets/d/12-hYpDkxA5CjfREcG9PdfLOMHeQJNFWAp2yo4mcxxlo/edit?gid=1350773495#gid=1350773495), phạm vi, phân công và các trường hợp kiểm thử.

Số liệu minh họa dùng kiểm chứng mô hình, chưa phải kết quả vận hành doanh nghiệp.
