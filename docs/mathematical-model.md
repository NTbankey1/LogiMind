# Mô hình toán học phân bổ đủ đơn hàng

Áp dụng **Policy A: phân bổ toàn bộ đơn hàng, mỗi đơn từ đúng một kho**. Mục tiêu duy nhất là tối thiểu hóa tổng chi phí giao trong các phương án đáp ứng đủ đơn, đúng tồn kho và công suất. Nếu không tồn tại phương án như vậy, bài toán không khả thi.

Tài liệu bàn giao gồm mô hình, Baseline, dữ liệu mẫu và đáp án kiểm chứng. Yêu cầu nghiệp vụ nằm trong [Yêu cầu hệ thống](requirements.md).

## 1. Tập hợp và tham số

Chữ hoa biểu diễn tập hợp, chữ thường là phần tử của tập.

| Ký hiệu | Ý nghĩa | Ví dụ |
|---|---|---|
| $I$ | Tập mọi đơn trong đợt | $I=\{A,B,C\}$ |
| $J$ | Tập kho | $J=\{K1,K2\}$ |
| $K$ | Tập mặt hàng | $K=\{X,Y\}$ |
| $E\subseteq I\times J$ | Các cặp đơn–kho được phép gán | Lập từ dữ liệu đầu đợt |
| $i\in I$, $j\in J$, $k\in K$ | Một đơn, một kho, một mặt hàng | $i=A$, $j=K1$, $k=X$ |

| Tham số | Ý nghĩa | Miền giá trị |
|---|---|---|
| $q_{ik}$ | Số sản phẩm loại k đơn i cần | Nguyên không âm |
| $s_{jk}$ | Tồn khả dụng mặt hàng k tại kho j | Nguyên không âm |
| $C_j$ | Số đơn tối đa kho j nhận trong đợt | Nguyên không âm |
| $c_{ij}$ | Chi phí giao nguyên đơn i từ kho j | Hữu hạn không âm với $(i,j)\in E$ |

Ví dụ $q_{1,2}=3$ nghĩa là đơn 1 cần 3 sản phẩm của mặt hàng 2. Chỉ số 2 là mã mặt hàng, không phải số lượng. $s_{1,2}=15$ nghĩa là kho 1 có 15 sản phẩm loại 2. $C_1=45$ nghĩa là kho 1 nhận tối đa 45 đơn.

Mỗi đơn có ít nhất một nhu cầu dương. Mỗi đơn chiếm 1 đơn vị công suất dù chứa nhiều sản phẩm. Tồn kho được kiểm tra riêng theo mặt hàng.

### Chi phí giao nguyên đơn

$c_{ij}$ lấy từ ma trận đầu vào, đã là chi phí của toàn bộ đơn. Đơn A có 3 sản phẩm và $c_{A,K2}=14$ thì gán A cho K2 đóng góp 14, không phải 42. Nhu cầu sản phẩm chỉ dùng trong ràng buộc tồn kho.

Ma trận được nhập hoặc sinh trước bằng dữ liệu mô phỏng có seed; mô hình không suy chi phí từ bản đồ, quãng đường hay trọng lượng. Không xét ghép tuyến, phí mở kho hoặc chiết khấu theo số đơn. Ghi đơn vị tiền cùng lần chạy; ví dụ dưới đây dùng nghìn đồng.

### Lập tập cặp hợp lệ E

Kiểm tra đầu vào trước khi dựng mô hình. Một cặp bị loại nếu thiếu chi phí, công suất kho bằng 0 hoặc kho không đủ một mặt hàng để phục vụ riêng nguyên đơn đó. Thiếu chi phí phải có cảnh báo, không tự thay bằng 0; đây là quy tắc dữ liệu cần thống nhất khi tích hợp.

$E$ được lập từ tồn kho đầu đợt, không dùng tồn kho sau Baseline. Sự cạnh tranh giữa các đơn được xử lý bằng ràng buộc tổng. Nếu một đơn không có cặp hợp lệ nào, có thể kết luận không khả thi ngay với nguyên nhân cụ thể.

## 2. Biến quyết định

Chỉ có biến phân bổ nhị phân:

$$
x_{ij}=\begin{cases}
1 & \text{nếu đơn }i\text{ giao từ kho }j,\\
0 & \text{ngược lại.}
\end{cases}
$$

Có thể tạo biến cho toàn bộ $I\times J$ rồi cố định bằng 0 ngoài $E$, hoặc chỉ tạo biến trên $E$. Các công thức dưới dùng cách thứ nhất, còn chi phí chỉ cộng trên $E$.

## 3. Mô hình Policy A

### 3.1. Hàm mục tiêu

$$
\min Z=\sum_{(i,j)\in E}c_{ij}x_{ij}.
$$

$Z$ bằng tổng chi phí giao toàn bộ đơn. `objective_value` và `shipping_cost` bằng nhau khi có phương án hợp lệ.

### 3.2. Giao đủ và không tách đơn

$$
\sum_{j\in J}x_{ij}=1\qquad\forall i\in I.
$$

Vế trái phải bằng đúng 1. Bằng 0 nghĩa là bỏ sót đơn; lớn hơn 1 nghĩa là gán một đơn nhiều kho. Cả hai đều không hợp lệ. Không thay dấu bằng bằng dấu nhỏ hơn hoặc bằng.

### 3.3. Không vượt tồn kho

$$
\sum_{i\in I}q_{ik}x_{ij}\le s_{jk}
\qquad\forall j\in J,\ \forall k\in K.
$$

Mỗi cặp kho–mặt hàng có một ràng buộc. Không cộng các loại hàng khác nhau thành một lượng tồn chung.

### 3.4. Không vượt công suất

$$
\sum_{i\in I}x_{ij}\le C_j\qquad\forall j\in J.
$$

Vế trái đếm số đơn, không phải số sản phẩm.

### 3.5. Miền biến và cặp bị cấm

$$
x_{ij}\in\{0,1\},\qquad x_{ij}=0\quad\forall(i,j)\notin E.
$$

Đây là mô hình tuyến tính nguyên nhị phân, giải được bằng bộ giải MILP. Không cần big-M cho các ràng buộc trên.

## 4. Kiểm tra khả thi và trạng thái bộ giải

Với $|I|$ là số đơn, các điều kiện cần gồm:

$$
\sum_{j\in J}C_j\ge |I|,\qquad
\sum_{j\in J}s_{jk}\ge\sum_{i\in I}q_{ik}\quad\forall k\in K.
$$

Vi phạm một điều kiện là đủ chứng minh không khả thi. Thỏa các điều kiện chưa đảm bảo có nghiệm vì không được tách đơn và tồn kho phân tán.

| Trạng thái | Điều kiện |
|---|---|
| `OPTIMAL` | Có phương án giao đủ, thỏa mọi ràng buộc và bộ giải chứng minh tối ưu |
| `FEASIBLE` | Có phương án giao đủ, chưa chứng minh tối ưu |
| `INFEASIBLE` | Bộ giải, vét cạn hoặc kiểm tra cần đã chứng minh không tồn tại phương án đầy đủ |
| `NO_SOLUTION_FOUND` | Chưa có phương án đầy đủ, chưa chứng minh không khả thi |
| `ERROR` | Lỗi dữ liệu, mô hình hoặc thực thi |

Hết thời gian có thể trả `FEASIBLE` nếu đã có nghiệm đầy đủ, hoặc `NO_SOLUTION_FOUND` nếu chưa có. Lưu lý do dừng riêng trong `termination_reason`. Khi không có phương án đầy đủ, chi phí kết quả chính để `null`, không để 0 và không dùng các gán tạm thời như một nghiệm hợp lệ.

## 5. Baseline

Sắp mã đơn theo chuỗi tăng dần, phân biệt hoa/thường; ví dụ `O10` đứng trước `O2`. Với mỗi đơn, chọn kho có chi phí thấp nhất còn đủ mọi mặt hàng và công suất. Khi bằng chi phí, chọn mã kho đứng trước theo cùng quy tắc chuỗi.

```text
stock_remaining = bản sao tồn kho gốc
capacity_remaining = bản sao công suất gốc
assignments = rỗng
for i in sorted(order_ids):
    candidates = các kho j có (i,j) thuộc E,
                 đủ mọi mặt hàng trong stock_remaining,
                 capacity_remaining[j] >= 1
    if candidates rỗng:
        return BASELINE_FAILED, chi phí chính = null,
               thông tin chẩn đoán đơn i và các gán tạm thời
    j = kho nhỏ nhất theo (shipping_cost[i,j], warehouse_id[j])
    gán i cho j
    trừ nhu cầu từng mặt hàng khỏi stock_remaining[j]
    capacity_remaining[j] -= 1
kiểm tra độc lập toàn bộ phương án
return FEASIBLE, assignments, tổng chi phí giao
```

Baseline thất bại không chứng minh bài toán vô nghiệm. Không trả `INFEASIBLE` chỉ vì thuật toán tham lam không tìm được kho cho một đơn. Xem ví dụ mục 8.3.

## 6. Ví dụ đầy đủ và kiểm chứng công thức

### 6.1. Dữ liệu đầu vào

$I=\{A,B,C\}$, $J=\{K1,K2\}$, $K=\{X,Y\}$. Chi phí tính bằng nghìn đồng.

| Đơn | Nhu cầu X | Nhu cầu Y |
|---|---:|---:|
| A | 2 | 1 |
| B | 1 | 2 |
| C | 2 | 0 |

| Kho | Tồn X | Tồn Y | Công suất |
|---|---:|---:|---:|
| K1 | 3 | 3 | 2 |
| K2 | 4 | 2 | 1 |

| Đơn | Chi phí K1 | Chi phí K2 |
|---|---:|---:|
| A | 10 | 14 |
| B | 11 | 12 |
| C | 9 | 25 |

Cả 6 cặp đơn–kho thuộc $E$. Trong công thức thay số, chỉ số 1 chỉ K1, chỉ số 2 chỉ K2.

### 6.2. Phương án được kiểm tra

Gán A → K2, B → K1, C → K1.

| Đơn | $x_{i1}$ | $x_{i2}$ |
|---|---:|---:|
| A | 0 | 1 |
| B | 1 | 0 |
| C | 1 | 0 |

### 6.3. Thay số vào hàm mục tiêu

$$
\begin{aligned}
Z&=10x_{A1}+14x_{A2}+11x_{B1}+12x_{B2}+9x_{C1}+25x_{C2}\\
 &=10(0)+14(1)+11(1)+12(0)+9(1)+25(0)=34.
\end{aligned}
$$

### 6.4. Kiểm tra giao đủ đơn

$$
\begin{aligned}
A:&\quad x_{A1}+x_{A2}=0+1=1,\\
B:&\quad x_{B1}+x_{B2}=1+0=1,\\
C:&\quad x_{C1}+x_{C2}=1+0=1.
\end{aligned}
$$

### 6.5. Kiểm tra tồn kho

$$
\begin{aligned}
K1,X:&\quad 2(0)+1(1)+2(1)=3\le3,\\
K1,Y:&\quad 1(0)+2(1)+0(1)=2\le3,\\
K2,X:&\quad 2(1)+1(0)+2(0)=2\le4,\\
K2,Y:&\quad 1(1)+2(0)+0(0)=1\le2.
\end{aligned}
$$

K1 còn X = 0, Y = 1; K2 còn X = 2, Y = 1.

### 6.6. Kiểm tra công suất

$$
K1:\ 0+1+1=2\le2,\qquad K2:\ 1+0+0=1\le1.
$$

K1 giao 5 sản phẩm trong 2 đơn nên tải xử lý bằng 2. Hai kho dùng 100% công suất. Toàn bộ biến là nhị phân và cả ba đơn được giao, nên phương án hợp lệ.

## 7. Chứng minh tối ưu và so sánh Baseline

Tổng công suất bằng 3. Muốn giao đủ 3 đơn, K1 phải nhận 2 đơn và K2 nhận 1 đơn. Chỉ có ba cách chọn đơn cho K2:

| Đơn tại K2 | Đơn tại K1 | Kết quả |
|---|---|---|
| A | B, C | Hợp lệ; chi phí $14+11+9=34$ |
| B | A, C | Không hợp lệ; K1 cần 4 sản phẩm X, chỉ có 3 |
| C | A, B | Hợp lệ; chi phí $25+10+11=46$ |

Đã xét hết các phương án có thể giao đủ đơn. Do đó giá trị tối ưu là 34.

Baseline xét A, B, C: A → K1, B → K1; sau đó K1 hết công suất, C → K2. Tổng chi phí bằng 46. Cả hai phương pháp đều có phương án đầy đủ hợp lệ nên tính được:

$$
\text{Giảm chi phí}=\frac{46-34}{46}\times100\%\approx26{,}09\%.
$$

Đây là kết quả của bộ dữ liệu minh họa, không đại diện cho mức cải thiện thực tế của toàn hệ thống.

## 8. Ví dụ lỗi phương án và không khả thi

### 8.1. Đủ công suất nhưng thiếu hàng

Dùng dữ liệu mục 6, gán A, C → K1 và B → K2. Công suất là 2 và 1, đều hợp lệ. Nhưng K1 cần $2+2=4$ sản phẩm X, vượt tồn 3. Phương án bị loại.

### 8.2. Đủ hàng nhưng vượt công suất

Gán A → K1 và B, C → K2. K2 cần X = 3, Y = 2, đều đủ tồn. Nhưng K2 nhận 2 đơn trong khi công suất chỉ bằng 1. Phương án bị loại.

### 8.3. Baseline thất bại nhưng vẫn có nghiệm

Một bộ dữ liệu riêng có 2 đơn, 2 kho, 2 mặt hàng:

| Đơn | Nhu cầu X | Nhu cầu Y | Chi phí K1 | Chi phí K2 |
|---|---:|---:|---:|---:|
| A | 1 | 0 | 1 | 2 |
| B | 0 | 1 | 1 | 3 |

| Kho | Tồn X | Tồn Y | Công suất |
|---|---:|---:|---:|
| K1 | 1 | 1 | 1 |
| K2 | 1 | 0 | 1 |

Baseline gán A → K1 vì chi phí 1 thấp hơn 2. Đến B, K1 hết công suất, K2 không có Y; Baseline trả `BASELINE_FAILED`. Chi phí gán tạm thời 1 không phải chi phí một phương án hợp lệ.

MILP có thể gán A → K2, B → K1, chi phí $2+1=3$. B bắt buộc ở K1 vì K2 không có Y, nên A phải ở K2; đây là nghiệm duy nhất và tối ưu.

### 8.4. Thiếu tổng công suất

Trở lại mục 6, chỉ đổi công suất K2 từ 1 thành 0. Tổng công suất là $2+0=2<3$ đơn. Vì mỗi đơn phải được giao và chiếm một công suất, không có phương án hợp lệ. Kết quả là `INFEASIBLE`; không trả việc giao riêng B, C như phương án hợp lệ. Chi phí kết quả chính là `null`.

### 8.5. Tổng hàng đủ nhưng đơn không thể tách

Một đơn A cần 2 sản phẩm X. K1 và K2 mỗi kho có 1 sản phẩm X, công suất 1; chi phí từ hai kho lần lượt là 10 và 12. Tổng X bằng nhu cầu 2 nhưng không kho nào đủ 2 sản phẩm để giao nguyên đơn. Bài toán `INFEASIBLE`.

### 8.6. Nhiều nghiệm tối ưu

Hai đơn A, B mỗi đơn cần 1 sản phẩm X. Hai kho mỗi kho có tồn X = 1 và công suất 1. Chi phí của mọi cặp đều bằng 10. Hai phương án A → K1, B → K2 và A → K2, B → K1 đều hợp lệ và có chi phí 20. Bộ kiểm thử phải chấp nhận cả hai.

## 9. Đầu ra và bộ kiểm tra độc lập

| Trường đề xuất | Nội dung |
|---|---|
| `algorithm`, `policy` | Phương pháp và `policy = A` |
| `assignments` | Khi thành công, mọi mã đơn ánh xạ đến đúng một mã kho |
| `shipping_cost`, `objective_value` | Cùng tổng chi phí giao của nghiệm đầy đủ; `null` nếu không có nghiệm |
| `remaining_stock`, `used_capacity` | Tồn theo SKU và số đơn của mỗi kho, tính từ nghiệm đầy đủ |
| `runtime_seconds` | Thời gian thuật toán, không gồm nạp dữ liệu, lưu hoặc vẽ giao diện |
| `solution_status`, `termination_reason` | Tình trạng nghiệm và lý do kết thúc |
| `best_bound`, `mip_gap` | Nếu bộ giải cung cấp; ghi định nghĩa gap của bộ giải |
| `diagnostics` | Thông tin lỗi hoặc gán tạm thời; không coi là nghiệm đầy đủ |

Tên trường cần được TV3 và TV5 đối chiếu khi tích hợp. Không đặt mã kho `null` trong một `assignments` được công bố là nghiệm hợp lệ. Khi không có nghiệm, có thể trả `assignments = null` và đưa chẩn đoán vào trường riêng.

Bộ kiểm tra độc lập của TV6 phải:

1. Kiểm tra phương án có đủ toàn bộ mã đơn trong đầu vào, không thừa, không thiếu và không lặp.
2. Mỗi đơn có đúng một kho tồn tại, cặp giao thuộc $E$; không tách đơn.
3. Tính lại nhu cầu từng SKU tại từng kho từ dữ liệu gốc và so với tồn.
4. Đếm số đơn tại từng kho và so với công suất.
5. Tính lại chi phí và nguồn lực còn lại; không chỉ tin số tổng thuật toán trả về.
6. Kiểm tra tính nguyên của nghiệm bộ giải theo dung sai đã chọn, rồi kiểm tra lại phân bổ rời rạc. Đề xuất dung sai chi phí $10^{-6}\max(1,|Z|)$ hoặc tính bằng đơn vị tiền nguyên nhỏ nhất.

Nếu bỏ sót một đơn, phương án không hợp lệ dù có chi phí thấp. Không dùng mẫu số là số đơn đã gán để che đơn bị thiếu.

Mức sử dụng công suất là số đơn đã gán chia $C_j$, nhân 100%; với $C_j=0$, ghi không áp dụng. Phương án hợp lệ luôn có tỷ lệ phục vụ 100%. Chỉ so sánh phần trăm giảm chi phí khi cả hai nghiệm đầy đủ hợp lệ và chi phí Baseline lớn hơn 0.

## 10. Điều kiện bàn giao và nguồn

- TV3 dựng mô hình chỉ với biến $x_{ij}$ và các tham số được định nghĩa tại mục 1.
- Bộ ví dụ mục 6 có đáp án tối ưu 34, Baseline 46.
- Mục 8.1 và 8.2 bị bộ kiểm tra loại bỏ.
- Mục 8.3 có tối ưu 3 dù Baseline thất bại.
- Mục 8.4 và 8.5 không khả thi; mục 8.6 có hai nghiệm tối ưu cùng 20.
- Khi MILP báo tối ưu trên dữ liệu nhỏ, đối chiếu với vét cạn. Thời gian giới hạn mà chưa có nghiệm không được đổi thành kết luận vô nghiệm.
- Lưu bộ giải, phiên bản dữ liệu, seed, đơn vị tiền, giới hạn thời gian và môi trường thực nghiệm.

Nguồn nghiệp vụ: [Tutorial Smart Logistics](https://docs.google.com/document/d/1ena1ZD8g8Emt3urDTUhlCquVawd5Pzar/edit), mục 3.1; [Sheet Group8](https://docs.google.com/spreadsheets/d/12-hYpDkxA5CjfREcG9PdfLOMHeQJNFWAp2yo4mcxxlo/edit?gid=1350773495#gid=1350773495) Chính sách của bản bàn giao này được cập nhật sang A theo yêu cầu mới.
