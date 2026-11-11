# Mô hình toán học phân bổ đơn hàng

Mô hình chính trình bày theo chính sách B: tối thiểu hóa chi phí giao cộng tiền phạt của đơn chưa phân bổ. B là phương án đề xuất trong bản TV1; nhóm cần duyệt chính sách và cách đặt phạt trước khi chốt kết quả thực nghiệm. Chính sách A được trình bày riêng tại mục 4.

Phương án TV1 đề nghị xác nhận: dùng B có phạt làm luồng chính, chi phí lấy theo nguyên đơn từ ma trận, bộ mô phỏng chuẩn ghi rõ phạt 100 nghìn đồng mỗi đơn và thử độ nhạy ở 50, 200. Chưa có xác nhận nhóm đã chấp thuận những quyết định này. Bảng quyết định nằm ở đầu `requirements.md`.

## 1. Tập hợp và tham số

Chữ hoa biểu diễn tập hợp; chữ thường là phần tử của tập.

| Ký hiệu | Ý nghĩa | Ví dụ |
|---|---|---|
| $I$ | Tập đơn hàng | $I=\{A,B,C\}$ |
| $J$ | Tập kho | $J=\{K1,K2\}$ |
| $K$ | Tập mặt hàng | $K=\{X,Y\}$ |
| $E\subseteq I\times J$ | Các cặp đơn–kho được phép giao | Chỉ gồm cặp có chi phí hợp lệ và đủ điều kiện đầu đợt |
| $i\in I$ | Một đơn hàng | $i=A$ |
| $j\in J$ | Một kho | $j=K1$ |
| $k\in K$ | Một mặt hàng | $k=X$ |

| Tham số | Ý nghĩa | Miền giá trị |
|---|---|---|
| $q_{ik}$ | Số sản phẩm loại $k$ đơn $i$ cần | Số nguyên không âm |
| $s_{jk}$ | Tồn khả dụng mặt hàng $k$ tại kho $j$ | Số nguyên không âm |
| $C_j$ | Số đơn tối đa kho $j$ nhận trong đợt | Số nguyên không âm |
| $c_{ij}$ | Chi phí giao toàn bộ đơn $i$ từ kho $j$ | Số hữu hạn không âm, với $(i,j)\in E$ |
| $P_i$ | Mức phạt nếu đơn $i$ chưa phân bổ | Số hữu hạn không âm |

Ví dụ $q_{1,2}=3$ nghĩa là đơn 1 cần **3 sản phẩm của mặt hàng 2**. Số 2 là chỉ số mặt hàng, số 3 là số lượng. $s_{1,2}=15$ nghĩa là kho 1 còn 15 sản phẩm của mặt hàng 2. $C_1=45$ nghĩa là kho 1 nhận tối đa 45 đơn trong đợt.

Mỗi đơn có ít nhất một mặt hàng có nhu cầu dương. Chi phí và phạt dùng cùng đơn vị tiền; ví dụ bên dưới dùng nghìn đồng. Một đơn luôn có tải xử lý bằng 1. Mô hình không gộp nhu cầu của các mặt hàng khác loại thành một giới hạn tồn kho chung.

### 1.1. Cách tính chi phí vận chuyển

$c_{ij}$ là chi phí giao toàn bộ đơn i từ kho j, đã có trong ma trận đầu vào. Tổng chi phí giao chỉ cộng những cặp được chọn:

$$
C_{\mathrm{ship}}=\sum_{(i,j)\in E}c_{ij}x_{ij}.
$$

Không nhân thêm $c_{ij}$ với $\sum_k q_{ik}$. Ví dụ A cần 2 sản phẩm X và 1 sản phẩm Y, có $c_{A,K2}=14$, gán A cho K2 đóng góp 14 nghìn đồng, không phải 42. Nhu cầu hàng chỉ đi vào ràng buộc tồn kho trong mô hình này.

Đây là giả định chi phí theo nguyên đơn, không có ghép tuyến hoặc phí mở kho. Ma trận được nhập hoặc sinh sẵn có seed; bản tối thiểu không suy chi phí từ tọa độ, quãng đường hay trọng lượng. Không trình bày số mô phỏng như báo giá vận tải thực tế.

### 1.2. Cách đặt phạt trong thí nghiệm

Đề nghị bộ mô phỏng chuẩn ghi rõ $P_i=100$ nghìn đồng cho mọi đơn. Các kịch bản độ nhạy dùng $P_i=50$ và $P_i=200$ trên cùng dữ liệu còn lại. Đây là lựa chọn tham số thí nghiệm để quan sát đánh đổi, chưa được hiệu chỉnh theo tổn thất thực tế. Với dữ liệu khác, nhận $P_i$ theo đơn và không tự điền giá trị thiếu.

Phạt được tính một lần mỗi đơn chưa phân bổ:

$$
C_{\mathrm{penalty}}=\sum_{i\in I}P_i u_i.
$$

Ví dụ một đơn có ba sản phẩm và phạt 100 thì bỏ nguyên đơn chịu phạt 100, không phải 300. Trong ví dụ mục 7.3, đổi phạt chung thành 50 cho mục tiêu tối ưu $20+50=70$; phạt 100 cho 120; phạt 200 cho 220. Cả ba trường hợp đều chọn giao B và C từ K1. Không phải mọi bộ dữ liệu đều giữ nguyên lựa chọn khi thay phạt.

Ví dụ khác: một đơn cần 1 sản phẩm X; mỗi kho có tồn X = 1 và công suất 1; chi phí từ K1 = 120, K2 = 150. Khi phạt 100, tối ưu là chưa giao và Z = 100; khi phạt 200, tối ưu là giao từ K1 và Z = 120. Ví dụ này kiểm tra trực tiếp ý nghĩa của chính sách B.

### Tiền xử lý

Kiểm tra đầu vào theo `requirements.md` trước khi tạo mô hình. Loại cặp đơn–kho khỏi $E$ nếu thiếu chi phí, công suất bằng 0 hoặc kho thiếu ít nhất một mặt hàng để xử lý riêng nguyên đơn đó. Cặp thiếu chi phí phải có cảnh báo; không thay bằng chi phí 0. Đây là quy tắc đề xuất kế thừa bản Word.

Không loại cặp chỉ vì các đơn khác có thể dùng hết hàng; việc cạnh tranh nguồn lực do các ràng buộc tổng giải quyết. Tập $E$ được lập từ dữ liệu đầu đợt, không lấy từ tồn kho còn lại sau khi chạy Baseline.

## 2. Biến quyết định

$$
x_{ij}=\begin{cases}
1 & \text{nếu đơn }i\text{ giao từ kho }j,\\
0 & \text{ngược lại.}
\end{cases}
$$

$$
u_i=\begin{cases}
1 & \text{nếu đơn }i\text{ chưa phân bổ},\\
0 & \text{nếu đơn đã được gán kho.}
\end{cases}
$$

Có thể tạo $x_{ij}$ cho toàn bộ $I\times J$ và cố định bằng 0 ngoài $E$, hoặc chỉ tạo biến cho $E$. Công thức dưới đây dùng cách thứ nhất để dễ đọc; chi phí chỉ cộng trên $E$.

## 3. Mô hình B

### 3.1. Hàm mục tiêu

$$
\min Z=\underbrace{\sum_{(i,j)\in E}c_{ij}x_{ij}}_{\text{chi phí giao}}
+\underbrace{\sum_{i\in I}P_i u_i}_{\text{tiền phạt}}.
$$

Đầu ra phải tách `shipping_cost`, `penalty_cost` và `objective_value`. Không gọi riêng chi phí giao là tổng mục tiêu trong B.

### 3.2. Mỗi đơn có đúng một trạng thái

$$
\sum_{j\in J}x_{ij}+u_i=1\qquad\forall i\in I.
$$

Đơn được giao từ đúng một kho hoặc chưa phân bổ. Không được vừa gán kho vừa đặt $u_i=1$.

### 3.3. Không vượt tồn kho

$$
\sum_{i\in I}q_{ik}x_{ij}\le s_{jk}
\qquad\forall j\in J,\ \forall k\in K.
$$

Mỗi cặp kho–mặt hàng có một ràng buộc riêng. Nếu có 2 kho và 2 mặt hàng thì có 4 ràng buộc tồn kho.

### 3.4. Không vượt công suất

$$
\sum_{i\in I}x_{ij}\le C_j\qquad\forall j\in J.
$$

Vế trái đếm số đơn được gán, không đếm số sản phẩm.

### 3.5. Tính hợp lệ của biến và cặp giao

$$
x_{ij},u_i\in\{0,1\},\qquad x_{ij}=0\quad\forall(i,j)\notin E.
$$

Đây là mô hình tuyến tính với biến nhị phân, có thể giải bằng bộ giải MILP. Không cần dùng big-M để biểu diễn các ràng buộc trên.

### 3.6. Ý nghĩa của mức phạt

Một đơn có chi phí giao thấp nhất 120 và phạt 100 có thể được để chưa phân bổ dù kho còn nguồn lực. Ngay cả khi chi phí riêng từng đơn thấp hơn phạt, cạnh tranh nguồn lực vẫn có thể khiến một số đơn bị bỏ lại trong phương án tối ưu toàn cục.

Không coi việc phạt lớn hơn từng chi phí giao là bằng chứng luôn tối đa hóa số đơn được giao. Nếu muốn ưu tiên phục vụ, dùng hai bước:

1. Tối thiểu hóa $U=\sum_i u_i$, thu được $U^*$ khi đã chứng minh tối ưu.
2. Bổ sung $\sum_i u_i=U^*$ rồi tối thiểu hóa chi phí giao.

Nếu bước 1 chưa chứng minh tối ưu thì chưa được khẳng định đã đạt số đơn phục vụ lớn nhất. Hai bước trên là biến thể khác của B có phạt, chỉ triển khai khi nhóm thống nhất.

Với đầu vào hợp lệ và chỉ các ràng buộc trong mục 3, đặt mọi $x=0$, mọi $u=1$ luôn tạo phương án hợp lệ. Nếu mô hình B báo không khả thi thì kiểm tra cách dựng mô hình và dữ liệu.

## 4. Biến thể chính sách A

Giữ ràng buộc tồn kho, công suất, miền nhị phân và cặp giao. Bỏ $u_i$ và tiền phạt, thay ràng buộc phân bổ bằng:

$$
\sum_{j\in J}x_{ij}=1\qquad\forall i\in I.
$$

Hàm mục tiêu là:

$$
\min Z_A=\sum_{(i,j)\in E}c_{ij}x_{ij}.
$$

Nếu không thể giao toàn bộ, A không có lời giải hợp lệ. Tổng tồn toàn mạng đủ và tổng công suất đủ chỉ là các điều kiện cần, không đảm bảo có nghiệm vì không tách đơn và tồn phân tán giữa các kho.

## 5. Baseline

Baseline không tìm tối ưu toàn cục. Phương pháp chọn kho rẻ nhất còn đủ nguồn lực theo thứ tự mã đơn. Sắp mã theo chuỗi tăng dần, phân biệt hoa/thường; mã số dạng chuỗi như `O10`, `O2` được sắp theo thứ tự chuỗi, không theo số. Nếu cần thứ tự khác phải đổi và ghi rõ cho mọi lần chạy.

Quy tắc dưới đây giữ đề xuất trong Word: với B, bỏ đơn nếu chi phí kho hợp lệ rẻ nhất lớn hơn phạt; nếu bằng nhau thì ưu tiên giao. Đây là phần bổ sung so với Baseline gán kho đơn thuần trong sheet nhóm, cần xác nhận khi duyệt mô hình.

```text
stock_remaining = bản sao tồn kho gốc
capacity_remaining = bản sao công suất gốc
for i in sorted(order_ids):
    candidates = các j có (i,j) thuộc E,
                 đủ stock_remaining cho mọi mặt hàng của i,
                 capacity_remaining[j] >= 1
    if candidates rỗng:
        ghi nhận i chưa phân bổ
        continue
    j = phần tử nhỏ nhất theo (shipping_cost[i,j], warehouse_id[j])
    if policy == B and shipping_cost[i,j] > penalty[i]:
        ghi nhận i chưa phân bổ
        continue
    gán i cho j
    trừ từng mặt hàng của i khỏi stock_remaining[j]
    capacity_remaining[j] -= 1
```

Với A, nếu Baseline còn đơn chưa phân bổ thì ghi **Baseline không tìm được phương án đầy đủ**. Điều này không chứng minh bài toán A không khả thi; cách tham lam có thể bỏ lỡ phương án tồn tại. Chỉ ghi `INFEASIBLE` khi bộ giải hoặc phép vét cạn đã chứng minh.

## 6. Ví dụ đầy đủ với 3 đơn và 2 mặt hàng

### 6.1. Dữ liệu

$I=\{A,B,C\}$, $J=\{K1,K2\}$, $K=\{X,Y\}$. Chi phí và phạt tính bằng nghìn đồng.

| Đơn | Nhu cầu X | Nhu cầu Y | Phạt |
|---|---:|---:|---:|
| A | 2 | 1 | 100 |
| B | 1 | 2 | 100 |
| C | 2 | 0 | 100 |

| Kho | Tồn X | Tồn Y | Công suất |
|---|---:|---:|---:|
| K1 | 3 | 3 | 2 |
| K2 | 4 | 2 | 1 |

| Đơn | Chi phí từ K1 | Chi phí từ K2 |
|---|---:|---:|
| A | 10 | 14 |
| B | 11 | 12 |
| C | 9 | 25 |

Tất cả 6 cặp đơn–kho đều thuộc $E$. Trong phần thay số, chỉ số 1 chỉ K1 và 2 chỉ K2.

### 6.2. Phương án và biến

Gán A cho K2, B và C cho K1:

| Đơn | $x_{i1}$ | $x_{i2}$ | $u_i$ |
|---|---:|---:|---:|
| A | 0 | 1 | 0 |
| B | 1 | 0 | 0 |
| C | 1 | 0 | 0 |

### 6.3. Thay số vào mục tiêu

$$
\begin{aligned}
Z={}&10x_{A1}+14x_{A2}+11x_{B1}+12x_{B2}\\
&+9x_{C1}+25x_{C2}+100u_A+100u_B+100u_C\\
={}&10(0)+14(1)+11(1)+12(0)+9(1)+25(0)\\
&+100(0)+100(0)+100(0)=34.
\end{aligned}
$$

Chi phí giao bằng 34; tiền phạt bằng 0.

### 6.4. Thay số vào ràng buộc

Mỗi đơn có đúng một trạng thái:

$$
\begin{aligned}
A:&\quad 0+1+0=1,\\
B:&\quad 1+0+0=1,\\
C:&\quad 1+0+0=1.
\end{aligned}
$$

Tồn kho theo thứ tự đơn A, B, C:

$$
\begin{aligned}
K1,X:&\quad 2(0)+1(1)+2(1)=3\le3,\\
K1,Y:&\quad 1(0)+2(1)+0(1)=2\le3,\\
K2,X:&\quad 2(1)+1(0)+2(0)=2\le4,\\
K2,Y:&\quad 1(1)+2(0)+0(0)=1\le2.
\end{aligned}
$$

Công suất:

$$
K1:\ 0+1+1=2\le2,\qquad K2:\ 1+0+0=1\le1.
$$

K1 còn X = 0, Y = 1; K2 còn X = 2, Y = 1. Hai kho đều dùng 100% công suất. K1 giao 5 sản phẩm trong 2 đơn nên tải xử lý là 2.

### 6.5. Chứng minh đáp án trên ví dụ

Muốn giao cả 3 đơn, K2 phải nhận đúng 1 đơn và K1 nhận 2 đơn:

| Đơn giao từ K2 | Hai đơn giao từ K1 | Kết quả |
|---|---|---|
| A | B và C | Hợp lệ; chi phí $14+11+9=34$ |
| B | A và C | Không hợp lệ; K1 cần 4 sản phẩm X nhưng chỉ có 3 |
| C | A và B | Hợp lệ; chi phí $25+10+11=46$ |

Mọi phương án bỏ ít nhất một đơn có tiền phạt từ 100 trở lên và chi phí giao không âm. Vì vậy đáp án tối ưu B là 34. Phương án này cũng tối ưu trong A.

Baseline lần lượt gán A → K1, B → K1, C → K2, chi phí 46. Hai phương pháp giao cùng tập đơn; mức giảm chi phí là $(46-34)/46\times100\%\approx26,09\%$.

## 7. Ví dụ vi phạm và thiếu nguồn lực

### 7.1. Đủ công suất nhưng thiếu hàng

Gán A, C → K1 và B → K2. Công suất là 2 và 1, đều hợp lệ. Tuy nhiên K1 cần $2+2=4$ sản phẩm X, vượt tồn 3. Phương án bị loại.

### 7.2. Đủ hàng nhưng vượt công suất

Gán A → K1 và B, C → K2. K2 dùng X = 3 và Y = 2, không vượt tồn. Nhưng K2 nhận 2 đơn, vượt công suất 1. Phương án bị loại.

### 7.3. K2 có công suất bằng 0

Chỉ đổi $C_{K2}=0$, giữ nguyên dữ liệu còn lại ở mục 6. K1 chỉ có thể nhận một trong hai cặp A, B hoặc B, C; cặp A, C thiếu X.

| Phương án | Chi phí giao | Tiền phạt | Mục tiêu B |
|---|---:|---:|---:|
| A, B → K1; C chưa phân bổ | 21 | 100 | 121 |
| B, C → K1; A chưa phân bổ | 20 | 100 | 120 |
| Chỉ C → K1 | 9 | 200 | 209 |
| Không giao đơn nào | 0 | 300 | 300 |

Trong các cách chỉ giao 1 đơn, C có chi phí nhỏ nhất. Bảng đủ để xác định tối ưu B là 120: A chưa phân bổ, B và C từ K1. Khi đó $x_{A1}=x_{A2}=0$, $u_A=1$ và $Z=11+9+100=120$. Tỷ lệ được giao là $2/3\approx66,67\%$.

Theo A, trường hợp này không khả thi vì tổng công suất 2 nhỏ hơn số đơn 3. Không so sánh riêng chi phí giao 20 với chi phí giao đủ đơn 34 để kết luận phương án nào tốt hơn.

### 7.4. Hai nghiệm tối ưu cùng chi phí

Hai đơn A, B mỗi đơn cần 1 sản phẩm X. K1 có tồn X = 1, công suất 1; K2 có tồn X = 0, công suất 1. Chi phí từ K1 của mỗi đơn đều là 10, mức phạt mỗi đơn là 100; chi phí từ K2 lần lượt là 11 và 30.

Giao A từ K1 hoặc giao B từ K1 đều cho $Z=110$. Cả hai nghiệm đều đúng. Không kiểm thử bằng yêu cầu một đơn cụ thể bắt buộc được chọn.

## 8. Đầu ra và kiểm tra độc lập

| Trường đề xuất | Nội dung |
|---|---|
| `algorithm`, `policy` | Phương pháp và chính sách |
| `assignments` | Mã đơn → mã kho hoặc `null` |
| `shipping_cost`, `penalty_cost`, `objective_value` | Ba khoản chi phí; A có phạt bằng 0 |
| `assigned_count`, `unassigned_count` | Số đơn được giao và chưa phân bổ |
| `remaining_stock`, `used_capacity` | Tồn còn lại theo SKU và số đơn từng kho |
| `runtime_seconds` | Thời gian thuật toán, ghi rõ phạm vi đo |
| `solution_status`, `termination_reason` | Tình trạng lời giải và lý do dừng |
| `best_bound`, `mip_gap` | Nếu bộ giải cung cấp; kèm định nghĩa gap của bộ giải |

Tên trường là đề xuất giao tiếp, cần TV3 và TV5 thống nhất với mã nguồn.

Phân biệt `OPTIMAL` (đã chứng minh tối ưu), `FEASIBLE` (có nghiệm chưa chứng minh tối ưu), `INFEASIBLE` (đã chứng minh vô nghiệm), `NO_SOLUTION_FOUND` (chưa tìm được nghiệm) và `ERROR`. Lý do dừng như giới hạn thời gian được ghi riêng. Không gán `OPTIMAL` cho Baseline; Baseline có thể trả `FEASIBLE`, hoặc `PARTIAL` trong A khi chưa giao hết.

Bộ kiểm tra độc lập phải:

1. Kiểm tra đủ các mã đơn, không lặp, không gán một đơn nhiều kho và chỉ dùng cặp thuộc $E$.
2. Với A, kiểm tra mọi đơn có kho; với B, kiểm tra $u_i$ khớp đơn chưa phân bổ.
3. Tính lại lượng dùng từng SKU tại từng kho từ dữ liệu gốc và đối chiếu tồn.
4. Đếm lại số đơn tại từng kho và đối chiếu công suất.
5. Tính lại chi phí giao, phạt, mục tiêu và tồn còn lại; không chỉ tin số tổng thuật toán trả về.
6. Nếu đọc biến thực từ bộ giải, dùng dung sai nhị phân phù hợp rồi kiểm tra lại phân bổ rời rạc. Đề xuất kiểm tra chi phí với sai số $10^{-6}\max(1,|Z|)$, hoặc tính chính xác bằng đơn vị tiền nguyên nhỏ nhất.

Mức sử dụng công suất là số đơn được gán chia $C_j$, nhân 100%. Khi $C_j=0$, ghi không áp dụng. Tỷ lệ phục vụ là số đơn được gán hợp lệ chia tổng số đơn; khi không có đơn, không thực hiện phép chia.

## 9. Điều kiện bàn giao mô hình

- TV3 dựng được mô hình từ dữ liệu đầu vào mà không phải tự đoán ý nghĩa tham số.
- Kết quả ví dụ mục 6 là 34, mục 7.3 là 120 trong B; mục 7.4 chấp nhận hai nghiệm cùng 110.
- Bộ kiểm tra phát hiện được cả hai phương án sai ở mục 7.1 và 7.2.
- T1–T9 trong `requirements.md` được đưa vào kế hoạch kiểm thử.
- Trên các bộ nhỏ, chỉ kết luận MILP tối ưu khi khớp giá trị vét cạn hoặc có chứng minh tương ứng.
- Chính sách, mức phạt, giới hạn thời gian, bộ giải và phiên bản dữ liệu được ghi cùng kết quả thực nghiệm.

## 10. Tài liệu nguồn

- [Tutorial chọn đề tài Smart Logistics](https://docs.google.com/document/d/1ena1ZD8g8Emt3urDTUhlCquVawd5Pzar/edit), mục 3.1.
- [Sheet Group8](https://docs.google.com/spreadsheets/d/12-hYpDkxA5CjfREcG9PdfLOMHeQJNFWAp2yo4mcxxlo/edit?gid=1350773495#gid=1350773495)

Các số liệu minh họa là dữ liệu giả định để kiểm chứng mô hình, chưa phải kết quả đo hiệu quả thực tế.
