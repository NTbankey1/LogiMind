# Hướng dẫn đóng góp cho LogiMind

Tài liệu này là thỏa thuận Git và cộng tác cho mọi người làm việc trên **LogiMind**. Nội dung áp dụng cho tất cả người đóng góp, bất kể làm ở phần nào của hệ thống:

- ứng dụng web frontend;
- API backend và cơ sở dữ liệu SQLite;
- engine tối ưu (heuristic baseline và bộ giải MILP);
- lớp dữ liệu, bao gồm bộ dữ liệu benchmark và fixture mẫu;
- tích hợp, kiểm thử và tài liệu.

Đọc [docs/project-overview.md](docs/project-overview.md) và [docs/architecture.md](docs/architecture.md) trước lần đóng góp đầu tiên. Thống nhất giao diện tại [docs/api-contract.md](docs/api-contract.md) và [docs/mathematical-model.md](docs/mathematical-model.md) trước khi cài đặt các module phụ thuộc.

---

## 1. Bảo vệ nhánh `main`

`main` là baseline dùng chung đã được review. Ruleset GitHub **Protect main branch** áp dụng cho nhánh này và không người đóng góp nào được bỏ qua:

- **Không bao giờ push trực tiếp vào `main`.** Mọi thay đổi, kể cả tài liệu và sửa lỗi nhỏ, đều phải đi qua Pull Request (PR).
- **PR cần ít nhất một review chấp thuận** từ người khác tác giả. GitHub không cho phép tự chấp thuận.
- **Mọi hội thoại review phải được giải quyết** trước khi merge.
- **Commit mới sẽ hủy các chấp thuận trước đó.** Sau khi push cập nhật, phải yêu cầu review lại.
- **Không thể xóa hoặc force-push `main`.** Lịch sử của nhánh không được viết lại.
- **PR phải nhắm tới `main`.** Merge commit, squash merge và rebase merge đều được phép; ưu tiên **Squash and merge** cho một thay đổi logic duy nhất để `main` dễ đọc.

Nhánh được bảo vệ là lưới an toàn, không thay thế review: người review vẫn phải kiểm tra tính đúng đắn, phạm vi và test.

---

## 2. Đặt tên nhánh

Tạo một nhánh cho mỗi nhiệm vụ, không phải cho mỗi người. Dùng mẫu `<type>/<short-description>` bằng tiếng Anh, chữ thường, kebab-case:

| Tiền tố | Dùng cho | Ví dụ |
| :--- | :--- | :--- |
| `feat/` | Tính năng hoặc module mới | `feat/milp-solver-adapter`, `feat/allocation-dashboard` |
| `fix/` | Sửa lỗi và sửa ràng buộc | `fix/capacity-overflow-check`, `fix/api-infeasible-response` |
| `docs/` | Chỉ tài liệu | `docs/clarify-infeasibility-status`, `docs/api-timeout-behavior` |
| `test/` | Bộ kiểm thử, fixture và dữ liệu test | `test/infeasible-capacity-fixtures` |
| `refactor/` | Tái cấu trúc nội bộ, không đổi hành vi | `refactor/extract-allocation-service` |
| `chore/` | Công cụ, CI, dependency, việc vặt | `chore/ci-json-validation` |

Giữ nhánh ngắn hạn. Không dùng lại nhánh sau khi PR đã merge và không tạo nhánh cá nhân (ví dụ `my-changes`).

---

## 3. Thông điệp commit

Mọi commit tuân theo [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<optional scope>): <short description>

[optional body: why the change is needed]

[optional footer: e.g. Closes #12]
```

- Viết mô tả ở thể mệnh lệnh, chữ thường, không có dấu chấm cuối: `add`, `fix`, `remove`, không dùng `added` hay `fixes`.
- Giữ dòng đầu khoảng 72 ký tự hoặc ít hơn.
- Mỗi commit là một thay đổi logic. Không trộn refactor, định dạng và hành vi mới trong cùng commit.
- Dùng scope khi cần làm rõ thành phần bị ảnh hưởng: `optimizer`, `api`, `db`, `ui`, `data`, `tests`, `docs`, `ci`.

| Loại | Mục đích | Ví dụ LogiMind |
| :--- | :--- | :--- |
| `feat` | Năng lực mới | `feat(optimizer): add allocation logic` |
| `fix` | Sửa lỗi hoặc ràng buộc | `fix(optimizer): prevent capacity overflow in baseline` |
| `docs` | Chỉ tài liệu | `docs: clarify infeasibility status` |
| `test` | Thêm hoặc cập nhật test | `test(optimizer): add infeasible capacity fixture` |
| `refactor` | Không đổi hành vi | `refactor(api): extract allocation service` |
| `chore` | Bảo trì và công cụ | `chore(ci): validate benchmark JSON fixtures` |

Khi PR được squash-merge, **tiêu đề PR** trở thành thông điệp commit trên `main`, nên tiêu đề PR cũng phải theo Conventional Commits.

---

## 4. Quy trình phát triển

### Bước 1: Đồng bộ với `main`

```bash
git checkout main
git pull --ff-only origin main
```

### Bước 2: Tạo nhánh nhiệm vụ

```bash
git checkout -b feat/your-task-description
```

### Bước 3: Triển khai thay đổi

Bám sát phạm vi nhiệm vụ. Không refactor module không liên quan và không thay đổi định nghĩa toán học khi chưa có đặc tả được thống nhất. Nếu thay đổi ảnh hưởng đến giao diện, cập nhật tài liệu hợp đồng trong cùng PR.

### Bước 4: Chạy test liên quan tại máy

Chạy các kiểm tra bao phủ phần đã sửa và sửa lỗi trước khi commit:

```bash
# Bộ kiểm thử tự động
pytest tests/ -v

# Kiểm tra cú pháp JSON của benchmark hoặc fixture mẫu
python -m json.tool data/samples/sample_small.json > /dev/null
python -m json.tool data/legacy/benchmark_data.json > /dev/null

# Chạy thử script phân bổ đơn
python scripts/validate_orders.py
```

Nếu một thành phần chưa có test, hãy nêu rõ trong PR thay vì tuyên bố đã kiểm chứng. Không báo test pass nếu chưa chạy tại máy hoặc trong CI.

### Bước 5: Tự review diff

```bash
git status --short
git diff
```

Xác nhận không có secret, file cơ sở dữ liệu, artifact sinh tự động hoặc thay đổi không liên quan.

### Bước 6: Stage và commit

```bash
git add <modified-files>
git commit -m "feat(optimizer): add allocation logic"
```

### Bước 7: Push nhánh

```bash
git push -u origin feat/your-task-description
```

### Bước 8: Mở Pull Request

Mở PR qua giao diện GitHub (hoặc `gh pr create --base main --head feat/your-task-description`) và điền đầy đủ [mẫu PR](.github/pull_request_template.md).

### Bước 9: Yêu cầu review và xử lý phản hồi

Yêu cầu ít nhất một người review. Trả lời mọi bình luận, push thay đổi được yêu cầu và yêu cầu review lại. Chỉ đánh dấu hội thoại đã giải quyết khi vấn đề được xử lý.

### Bước 10: Merge và dọn dẹp

Sau khi được chấp thuận, CI xanh và mọi hội thoại đã giải quyết, merge PR. Sau đó xóa nhánh:

```bash
git push origin --delete feat/your-task-description
git branch -d feat/your-task-description
```

---

## 5. Kỳ vọng với Pull Request

Người review phải hiểu và kiểm chứng được PR mà không cần đọc toàn bộ codebase. Mọi PR phải:

- **Nêu mục đích và phạm vi** — giải quyết vấn đề gì và chủ động không thay đổi gì.
- **Liên kết issue hoặc nhiệm vụ** — ví dụ `Closes #12`.
- **Liệt kê thành phần đã sửa** — frontend, backend/API, schema SQLite, engine tối ưu (baseline hoặc MILP), fixture dữ liệu, test hoặc tài liệu.
- **Kèm kết quả test** — lệnh đã chạy và kết quả, hoặc nêu rõ vì sao không thể chạy.
- **Ghi chú rủi ro và hạn chế** — timeout bộ giải, edge case chưa xử lý hoặc việc tiếp theo.

Giữ PR tập trung và dễ review. Chia thay đổi lớn thành nhiều PR nhỏ thay vì gộp việc không liên quan.

### Quy tắc CI và review

[Workflow CI](.github/workflows/ci.yml) kiểm tra fixture JSON, liên kết Markdown nội bộ và các file thiết yếu của repository. CI phải xanh trước khi merge. Ruleset hiện yêu cầu phê duyệt của người và giải quyết hội thoại; **chưa** yêu cầu status check CI, nên người review phải tự xác nhận kết quả CI.

Trước khi merge:

- [ ] Có ít nhất một phê duyệt từ người khác tác giả.
- [ ] Mọi hội thoại review đã giải quyết.
- [ ] CI pass.
- [ ] Nhánh đã cập nhật với `main` và xung đột đã xử lý.
- [ ] Không commit secret, file cơ sở dữ liệu hoặc artifact sinh tự động.

---

## 6. Đồng bộ nhánh và xử lý xung đột

Khi `main` tiến lên trong lúc nhánh đang mở, cập nhật nhánh trước khi yêu cầu review cuối.

### Cách A: Merge `main` vào nhánh (khuyến nghị)

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git checkout feat/your-task-description
git merge main
```

### Cách B: Rebase lên `main`

Chỉ dùng khi bạn thoải mái viết lại lịch sử nhánh của chính mình:

```bash
git fetch origin
git checkout feat/your-task-description
git rebase origin/main
git push --force-with-lease origin feat/your-task-description
```

`--force-with-lease` chỉ chấp nhận **trên nhánh nhiệm vụ của chính bạn**. Không bao giờ force-push `main` và không viết lại nhánh người khác đang làm việc.

### Xử lý xung đột an toàn

1. Chạy `git status` để liệt kê file xung đột.
2. Mở từng file và tìm dấu xung đột:

   ```text
   <<<<<<< HEAD
   changes already on your branch
   =======
   changes coming from main
   >>>>>>> main
   ```

3. Sửa file để tích hợp đúng cả hai bên, sau đó xóa mọi dòng đánh dấu.
4. Stage các file đã giải quyết:

   ```bash
   git add <resolved-files>
   ```

5. Hoàn tất thao tác:
   - Sau merge: `git commit` (tạo merge commit).
   - Sau rebase: `git rebase --continue`.
6. **Chạy lại test liên quan** để xác nhận việc giải quyết không làm hỏng gì.
7. Push nhánh và yêu cầu review mới — lần push đã hủy phê duyệt trước đó.

Nếu xung đột quá phức tạp, hãy hủy và làm lại thay vì commit một bản giải quyết dở dang:

```bash
git merge --abort     # hoặc: git rebase --abort
```

Không giải quyết xung đột bằng cách xóa code bạn không hiểu. Khi không chắc, hãy hỏi tác giả của thay đổi đến.

---

## 7. Bảo mật và vệ sinh repository

- **Không bao giờ commit secret.** Bao gồm mật khẩu, API key, access token, chứng chỉ và file `.env`. Sao chép [.env.example](.env.example) thành `.env` tại máy và giữ `.env` ngoài Git.
- **Không commit file cơ sở dữ liệu** (`*.db`, `*.sqlite`, `*.sqlite3`) hoặc dữ liệu sinh tự động. Chỉ fixture đã được duyệt trong `data/samples/` thuộc về Git; giữ dữ liệu lớn hoặc sinh tự động trong `data/raw/` hoặc `data/processed/` tại máy.
- **Tránh file sinh tự động và binary lớn không cần thiết.** Không thêm build output, cache, log, archive hoặc tài liệu không thuộc hạng mục bàn giao.
- **Không thêm file của editor, hệ điều hành hoặc môi trường ảo** (`.venv/`, `.vscode/`, `.idea/`, `.DS_Store`). Chúng đã có trong `.gitignore`.
- **Kiểm tra nội dung stage** trước mỗi commit:

  ```bash
  git status --short
  git diff --cached --stat
  ```

Nếu lỡ commit secret, hãy thu hồi hoặc xoay khóa ngay và thông báo cho người duy trì. Xóa secret trong commit sau không loại bỏ nó khỏi lịch sử repository.

---

## 8. Tài liệu liên quan

| Tài liệu | Mục đích |
| :--- | :--- |
| [docs/project-overview.md](docs/project-overview.md) | Bối cảnh bài toán, phạm vi và mục tiêu |
| [docs/architecture.md](docs/architecture.md) | Thành phần, luồng dữ liệu và công nghệ |
| [docs/api-contract.md](docs/api-contract.md) | Hợp đồng yêu cầu/phản hồi giữa frontend và backend |
| [docs/mathematical-model.md](docs/mathematical-model.md) | Mô hình MILP và định nghĩa ràng buộc |
| [docs/data-dictionary.md](docs/data-dictionary.md) | Schema bộ dữ liệu và định nghĩa trường |
| [docs/testing-strategy.md](docs/testing-strategy.md) | Các bậc test, bất biến và edge case bắt buộc |
| [docs/glossary.md](docs/glossary.md) | Thuật ngữ Việt–Anh dùng thống nhất |
| [.github/pull_request_template.md](.github/pull_request_template.md) | Cấu trúc PR bắt buộc |
| [data/README.md](data/README.md) | Quy tắc quản lý bộ dữ liệu |
