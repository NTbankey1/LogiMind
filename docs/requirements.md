# Yêu cầu hệ thống LogiMind

LogiMind hỗ trợ phân bổ đơn hàng giữa 2–3 kho có giới hạn tồn kho và công suất xử lý. Hệ thống so sánh cách phân bổ tuần tự (Baseline) với mô hình tối ưu MILP trên cùng dữ liệu.

Tài liệu này mô tả yêu cầu nghiệp vụ và điều kiện nghiệm thu. Công thức, ví dụ tính tay và hướng dẫn triển khai thuật toán nằm trong [Mô hình toán học](mathematical-model.md).

> **Cập nhật chính sách (2026-11-11):** Project Lead đã chọn **Chính sách A** làm chính sách chuẩn, ghi tại [ADR-004](decisions/0004-allocation-policy-a.md). Hợp đồng dữ liệu chuẩn của TV2 là Policy A và được mô tả tại [Data Dictionary](data-dictionary.md). Các mục mô tả Chính sách B trong tài liệu này được giữ làm tham chiếu lịch sử, không phải hợp đồng triển khai.

## 1. Người sử dụng và bài toán

Nhân viên điều phối nhập tập đơn của một đợt, chạy phân bổ và xem kho xử lý từng đơn. Quản lý kho xem lượng tồn và công suất đã sử dụng.

Chọn kho rẻ nhất cho từng đơn có thể làm hết hàng hoặc công suất tại kho đó, khiến các đơn tiếp theo phải giao từ kho đắt hơn. Hệ thống cần xét đồng thời nguồn lực và chi phí của toàn bộ đợt phân bổ.

## 2. Phạm vi và giả định

- Dùng dữ liệu mô phỏng, có seed cố định để tái lập.
- Một đợt có 2–3 kho; một đơn có thể chứa nhiều mặt hàng.
- Một đơn được giao nguyên vẹn từ một kho, không tách đơn.
- Tồn kho là lượng khả dụng đầu đợt; không nhập thêm hàng hoặc chuyển hàng giữa các kho trong khi tính phương án.
- Công suất là số đơn tối đa một kho xử lý trong đợt. Mỗi đơn có tải bằng 1, không phụ thuộc số sản phẩm trong đơn.
- Chi phí giao toàn bộ một đơn từ một kho được cung cấp sẵn trong ma trận, dùng cùng đơn vị tiền với mức phạt.
- Mỗi lần chạy tính trên bản sao dữ liệu đầu vào. So sánh hai thuật toán không được dùng tồn kho đã bị thuật toán trước trừ đi.
- Kết quả là kế hoạch đề xuất; chạy thuật toán không đồng nghĩa đã xuất hàng thực tế.

Ngoài phạm vi: tối ưu tuyến xe nhiều điểm, dự báo nhu cầu, thanh toán, quản trị nhân sự, tích hợp WMS/ERP và dữ liệu thời gian thực.

## 3. Chính sách phân bổ

| Nội dung | Chính sách A | Chính sách B |
|---|---|---|
| Yêu cầu giao hết đơn | Bắt buộc | Không bắt buộc |
| Đơn chưa phân bổ | Không được phép trong lời giải hợp lệ | Được phép, có phạt theo đơn |
| Hàm mục tiêu | Chi phí giao hàng | Chi phí giao hàng cộng tiền phạt |
| Khi nguồn lực không đủ | Có thể không khả thi | Có thể trả phương án có đơn chưa phân bổ |

Bản bàn giao ban đầu đề xuất B làm chính sách chính, phù hợp với nội dung đã trình bày trong Word. Tuy nhiên, ngày 2026-11-11 Project Lead đã chọn **A** làm chính sách chuẩn ([ADR-004](decisions/0004-allocation-policy-a.md)); phần B dưới đây chỉ còn là tham chiếu lịch sử. Nhóm vẫn cần thống nhất cách đặt mức phạt nếu B được dùng trong thực nghiệm so sánh.

Trong B, `penalty` phải có trong dữ liệu từng đơn. Không tự coi đơn chưa giao có chi phí bằng 0, không tự đặt mức phạt 100 cho mọi dữ liệu. Giá trị 100 chỉ dùng trong các ví dụ.

Nếu mức phạt thấp hơn chi phí giao, mô hình có thể để đơn chưa phân bổ dù còn nguồn lực. Nếu nhóm muốn ưu tiên giao nhiều đơn nhất, cần đổi sang mục tiêu hai bước được mô tả trong tài liệu mô hình và ghi rõ thay đổi này.

## 4. Dữ liệu đầu vào

Tên trường dưới đây là đề xuất thống nhất giữa TV2, TV3 và TV5, chưa phải mô tả API đã có trong repository.

| Dữ liệu | Trường | Ý nghĩa |
|---|---|---|
| Đơn hàng | `order_id`, `penalty` | Mã đơn duy nhất và mức phạt của đơn trong B |
| Dòng hàng | `order_id`, `sku_id`, `quantity` | Mặt hàng và số lượng đơn cần |
| Kho | `warehouse_id`, `capacity` | Mã kho duy nhất và công suất trong đợt |
| Danh mục hàng | `sku_id` | Mã mặt hàng duy nhất |
| Tồn kho | `warehouse_id`, `sku_id`, `stock` | Số lượng khả dụng đầu đợt |
| Chi phí | `order_id`, `warehouse_id`, `shipping_cost` | Chi phí giao nguyên đơn từ kho |
| Cấu hình chạy | `policy`, `time_limit_seconds`, `seed` | Chính sách, giới hạn thời gian và seed nếu sinh dữ liệu |

> Với hợp đồng dữ liệu chuẩn **Policy A** của TV2, `penalty` không tồn tại trong dataset; cấu trúc chuẩn là `data/schema/dataset.schema.json`. Bảng trường trên đây mô tả mô hình khái niệm dùng chung cho cả A và B.

### Quy tắc kiểm tra

1. Mã không được trống; các mã tham chiếu phải tồn tại. Không chấp nhận mã đơn trùng, dòng tồn kho trùng cặp kho–mặt hàng hoặc chi phí trùng cặp đơn–kho.
2. Mỗi đơn có ít nhất một dòng hàng. `quantity` là số nguyên dương; dòng hàng trùng cặp đơn–mặt hàng bị báo lỗi để tránh cộng hai lần ngoài ý muốn.
3. `stock` và `capacity` là số nguyên không âm; 0 là giá trị hợp lệ. Chi phí và mức phạt là số hữu hạn không âm; không nhận NaN hoặc vô cực.
4. Bảng tồn phải đủ các cặp kho–mặt hàng trong phạm vi dữ liệu. Không có hàng phải ghi 0; ô thiếu không tự hiểu là 0.
5. Một đơn không có mặt hàng nào đó được biểu diễn bằng nhu cầu 0 trong mô hình; không cần tạo dòng hàng có số lượng 0.
6. Cặp đơn–kho thiếu chi phí được loại khỏi lựa chọn, kèm cảnh báo rõ. Chi phí âm hoặc sai kiểu dữ liệu là lỗi, không được coi như cặp bị cấm. Cách xử lý thiếu chi phí này là đề xuất kế thừa bản Word, cần nhóm xác nhận.
7. Nhu cầu vượt nguồn lực là tình huống bài toán, không phải lỗi định dạng. Trong A có thể dẫn đến không khả thi; trong B có thể có đơn chưa phân bổ.

## 5. Yêu cầu chức năng

| Mã | Yêu cầu | Điều kiện nghiệm thu |
|---|---|---|
| FR01 | Nhập hoặc tải dữ liệu | Đọc được đơn, dòng hàng, kho, tồn kho và chi phí; thông báo bản ghi sai |
| FR02 | Xem dữ liệu trước khi chạy | Hiển thị số đơn, số kho, danh mục hàng, tồn kho, công suất và cảnh báo |
| FR03 | Chạy Baseline | Xử lý mã đơn tăng dần, chọn kho hợp lệ rẻ nhất và cập nhật nguồn lực trong bản sao dữ liệu |
| FR04 | Chạy MILP | Dùng đúng mô hình, chính sách và giới hạn thời gian; trả trạng thái lời giải |
| FR05 | Kiểm tra độc lập kết quả | Phát hiện tách đơn, trùng phân bổ, thiếu hàng, vượt công suất và sai tổng chi phí |
| FR06 | Xem kết quả | Hiển thị kho của từng đơn hoặc chưa phân bổ, chi phí giao, tiền phạt, tổng mục tiêu và nguồn lực còn lại |
| FR07 | So sánh hai phương pháp | Cùng dữ liệu gốc, cùng chính sách và mức phạt; có số đơn được giao, chi phí, thời gian và trạng thái |
| FR08 | Lưu và đọc lại kết quả | Nếu lưu SQLite, kết quả đọc lại giữ nguyên dữ liệu chạy, cấu hình, phân bổ và các chỉ số |

Xuất CSV/Excel, tách đơn, công suất theo khối lượng và chi phí mở kho là phần mở rộng, thực hiện sau phạm vi bắt buộc.

## 6. Quy tắc kết quả và lỗi

- Phân biệt phương án hợp lệ với phương án đã chứng minh tối ưu. Đơn chưa phân bổ trong B vẫn có thể thuộc phương án hợp lệ, thậm chí tối ưu.
- Hết thời gian mà có lời giải hợp lệ thì hiển thị phương án tốt nhất tìm được cùng trạng thái chưa chứng minh tối ưu. Không có lời giải thì không hiển thị phương án rỗng như kết quả tối ưu.
- Trong B, nếu đầu vào hợp lệ và không có ràng buộc bổ sung, phương án để tất cả đơn chưa phân bổ luôn hợp lệ. Bộ giải báo không khả thi trong trường hợp này cần được kiểm tra lại mô hình.
- Nguyên nhân chưa phân bổ phải có căn cứ. Không gán chung lý do “thiếu hàng” cho mọi đơn; có thể do công suất, cạnh tranh nguồn lực hoặc mức phạt.
- Thuật toán không được sửa dữ liệu đầu vào dùng chung. Nạp lại cùng dữ liệu và cấu hình phải tạo được cùng bài toán.
- Baseline dùng quy tắc phá hòa cố định. MILP có thể trả các phân bổ khác nhau nếu có nhiều nghiệm tối ưu; bộ kiểm tra xét tính hợp lệ và giá trị mục tiêu.

## 7. Kiểm thử và đánh giá

| Mã | Tình huống | Kết quả cần kiểm tra |
|---|---|---|
| T1 | Ví dụ nhỏ tính tay | Chi phí và phương án hợp lệ khớp tính tay hoặc vét cạn |
| T2 | Đủ tồn kho và công suất | Có thể giao toàn bộ; với B còn phụ thuộc mức phạt |
| T3 | Kho rẻ nhất thiếu một mặt hàng | Không gán nguyên đơn cho kho đó |
| T4 | Kho rẻ nhất hết công suất | Không vượt công suất; dùng kho khác hoặc chưa phân bổ |
| T5 | Tồn kho và công suất đều chặt | Đồng thời thỏa mãn mọi ràng buộc |
| T6 | Không thể giao hết đơn | A không có nghiệm đầy đủ; B ghi nhận đơn chưa phân bổ và tiền phạt |
| T7 | Dữ liệu lỗi | Báo đúng mã hoặc trường sai; không chạy trên dữ liệu chưa hợp lệ |
| T8 | Các kho bằng chi phí | Baseline phá hòa theo mã kho; chấp nhận nhiều nghiệm tối ưu của MILP |
| T9 | Tăng quy mô số đơn | Ghi thời gian, trạng thái và chất lượng lời giải dưới giới hạn thời gian |

Thu thập chi phí giao, tiền phạt, giá trị mục tiêu, số đơn được giao/chưa phân bổ, tỷ lệ hợp lệ, mức sử dụng công suất và thời gian. Đo thời gian thuật toán tách khỏi thời gian tải dữ liệu, lưu cơ sở dữ liệu và vẽ giao diện.

Chỉ so sánh trực tiếp phần trăm giảm chi phí giao khi hai phương pháp phục vụ cùng tập đơn và chi phí Baseline lớn hơn 0. Nếu tập đơn khác nhau, báo cáo thêm tỷ lệ phục vụ và tổng mục tiêu. Không rút kết luận hiệu quả thực tế chỉ từ dữ liệu mô phỏng.

## 8. Bàn giao giữa các thành viên

| Thành viên | Nội dung cần phối hợp |
|---|---|
| TV1 | Giải thích nghiệp vụ, công thức, giả định và đáp án ví dụ; phân tích kết quả |
| TV2 | Thống nhất cấu trúc dữ liệu, seed, T1–T9 và chương trình vét cạn |
| TV3 | Triển khai Baseline/MILP theo mô hình; trả trạng thái và các chỉ số |
| TV4 | Hiển thị dữ liệu, cảnh báo, kết quả và so sánh |
| TV5 | API, SQLite, tích hợp thuật toán và lưu cấu hình chạy |
| TV6 | Kiểm tra độc lập ràng buộc, tích hợp và tổng hợp kiểm thử |

Chính sách đã chốt là **A** ([ADR-004](decisions/0004-allocation-policy-a.md)). Trước khi triển khai vẫn cần xác nhận cách đặt mức phạt nếu dùng B cho so sánh, quy tắc thiếu chi phí, quy tắc phá hòa và giới hạn thời gian. Trước khi kết luận thực nghiệm cần ghi phiên bản bộ giải và môi trường chạy.

## 9. Tài liệu nguồn

- [Tutorial chọn đề tài Smart Logistics](https://docs.google.com/document/d/1ena1ZD8g8Emt3urDTUhlCquVawd5Pzar/edit), mục 3.1 và các mục 6–9.
- [Đăng ký và phân công nhóm 8](https://docs.google.com/spreadsheets/d/12-hYpDkxA5CjfREcG9PdfLOMHeQJNFWAp2yo4mcxxlo/edit?gid=1350773495#gid=1350773495).

Hai tài liệu Markdown được chuyển soạn từ phần phân tích TV1 và thống nhất thuật ngữ để phục vụ triển khai. Các quy tắc còn ở mức đề xuất đã được ghi rõ ở trên.
