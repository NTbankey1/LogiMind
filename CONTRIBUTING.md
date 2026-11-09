# Contributing to LogiMind

This document is the Git and collaboration agreement for everyone working on **LogiMind**. It applies to all contributors, regardless of which part of the system they work on:

- the frontend web application;
- the backend API and its SQLite database;
- the optimization engine (baseline heuristics and the MILP solver);
- the data layer, including benchmark datasets and sample fixtures;
- integration, testing, and documentation.

Read [docs/project-overview.md](docs/project-overview.md) and [docs/architecture.md](docs/architecture.md) before your first contribution. Agree on interfaces in [docs/api-contract.md](docs/api-contract.md) and [docs/mathematical-model.md](docs/mathematical-model.md) before implementing dependent modules.

---

## 1. Branch protection on `main`

`main` is the shared, reviewed baseline. The GitHub ruleset **Protect main branch** applies to it and cannot be bypassed by any contributor:

- **Never push directly to `main`.** Every change, including documentation and small fixes, goes through a Pull Request (PR).
- **A PR requires at least one approving review** from someone other than its author. Self-approval is not possible on GitHub.
- **All review conversations must be resolved** before the PR can be merged.
- **New commits dismiss previous approvals.** After pushing updates, request a fresh review.
- **`main` cannot be deleted or force-pushed.** Its history cannot be rewritten.
- **Pull Requests target `main`.** Merge commits, squash merges, and rebase merges are all permitted; prefer **Squash and merge** for a single logical change so `main` stays readable.

Protected branches are a safety net, not a review substitute: reviewers are expected to check correctness, scope, and tests.

---

## 2. Branch naming

Create one branch per task, not per person. Use the pattern `<type>/<short-description>` in lower-case kebab-case English:

| Prefix | Use for | Example |
| :--- | :--- | :--- |
| `feat/` | New features or modules | `feat/milp-solver-adapter`, `feat/allocation-dashboard` |
| `fix/` | Bug fixes and constraint corrections | `fix/capacity-overflow-check`, `fix/api-infeasible-response` |
| `docs/` | Documentation only | `docs/clarify-split-penalty`, `docs/api-timeout-behavior` |
| `test/` | Test suites, fixtures, and test data | `test/infeasible-capacity-fixtures` |
| `refactor/` | Internal restructuring with no behavior change | `refactor/extract-allocation-service` |
| `chore/` | Tooling, CI, dependencies, housekeeping | `chore/ci-json-validation` |

Keep branches short-lived. Do not reuse a branch after its PR is merged, and do not create personal branches (for example, `my-changes`).

---

## 3. Commit messages

All commits follow [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<optional scope>): <short description>

[optional body: why the change is needed]

[optional footer: e.g. Closes #12]
```

- Write the description in the imperative mood, lower-case, without a trailing period: `add`, `fix`, `remove`, not `added` or `fixes`.
- Keep the first line at roughly 72 characters or fewer.
- Make one logical change per commit. Do not mix refactoring, formatting, and new behavior in the same commit.
- Use a scope when it clarifies the affected component: `optimizer`, `api`, `db`, `ui`, `data`, `tests`, `docs`, `ci`.

| Type | Purpose | LogiMind example |
| :--- | :--- | :--- |
| `feat` | New capability | `feat(optimizer): add allocation logic` |
| `fix` | Bug or constraint correction | `fix(optimizer): prevent capacity overflow in baseline` |
| `docs` | Documentation only | `docs: clarify split-shipment penalty` |
| `test` | Adding or updating tests | `test(optimizer): add infeasible capacity fixture` |
| `refactor` | No behavior change | `refactor(api): extract allocation service` |
| `chore` | Maintenance and tooling | `chore(ci): validate benchmark JSON fixtures` |

When a PR is squash-merged, its **PR title** becomes the commit message on `main`, so keep the PR title in Conventional Commits form as well.

---

## 4. Development workflow

### Step 1: Synchronize with `main`

```bash
git checkout main
git pull --ff-only origin main
```

### Step 2: Create a task branch

```bash
git checkout -b feat/your-task-description
```

### Step 3: Implement your changes

Stay within the scope of the task. Do not refactor unrelated modules or change mathematical definitions without an agreed specification. If your change affects an interface, update the contract documentation in the same PR.

### Step 4: Run the relevant tests locally

Run the checks that cover what you changed, and fix failures before committing:

```bash
# Automated test suite (once test files are present)
pytest tests/ -v

# Validate JSON benchmark or sample fixtures
python -m json.tool data/samples/sample_small.json > /dev/null

# Smoke-check the order-allocation script
python validate_orders.py
```

If a component has no tests yet, state that explicitly in the PR instead of claiming the change was verified. Do not report a test as passing unless you ran it locally or in CI.

### Step 5: Review your own diff

```bash
git status --short
git diff
```

Confirm that no secrets, database files, generated artifacts, or unrelated edits are included.

### Step 6: Stage and commit

```bash
git add <modified-files>
git commit -m "feat(optimizer): add allocation logic"
```

### Step 7: Push the branch

```bash
git push -u origin feat/your-task-description
```

### Step 8: Open a Pull Request

Open a PR through the GitHub interface (or with `gh pr create --base main --head feat/your-task-description`) and complete [the PR template](.github/pull_request_template.md) in full.

### Step 9: Request review and address feedback

Request at least one reviewer. Respond to every comment, push the requested changes, and re-request review. Resolve conversations only once the concern is addressed.

### Step 10: Merge and clean up

After approval, a green CI run, and resolved conversations, merge the PR. Then delete the branch:

```bash
git push origin --delete feat/your-task-description
git branch -d feat/your-task-description
```

---

## 5. Pull Request expectations

A reviewer should be able to understand and verify a PR without reading the entire codebase. Every PR must:

- **Explain purpose and scope** — what problem it solves and what it deliberately does not change.
- **Link the related issue or task** — for example `Closes #12`.
- **List the modified components** — frontend, backend/API, SQLite schema, optimization engine (baseline or MILP), data fixtures, tests, or documentation.
- **Include test results** — the commands executed and their outcome, or a clear statement that tests could not be run and why.
- **Note risks and limitations** — solver timeouts, unhandled edge cases, or follow-up work.

Keep PRs focused and reviewable. Split large changes into a sequence of smaller PRs rather than bundling unrelated work.

### CI and review rules

The [CI workflow](.github/workflows/ci.yml) validates JSON fixtures, internal Markdown links, and essential repository files. CI must be green before a PR is merged. The ruleset currently requires human approval and conversation resolution; it does **not** yet require a CI status check, so reviewers must confirm CI results themselves.

Before merging:

- [ ] At least one approval from a contributor other than the author.
- [ ] Every review conversation resolved.
- [ ] CI passing.
- [ ] Branch up to date with `main` and conflicts resolved.
- [ ] No secrets, database files, or generated artifacts committed.

---

## 6. Keeping your branch in sync and resolving conflicts

When `main` advances while your branch is open, update it before requesting a final review.

### Option A: Merge `main` into your branch (recommended)

```bash
git fetch origin
git checkout main
git pull --ff-only origin main
git checkout feat/your-task-description
git merge main
```

### Option B: Rebase onto `main`

Use this only if you are comfortable rewriting your own branch history:

```bash
git fetch origin
git checkout feat/your-task-description
git rebase origin/main
git push --force-with-lease origin feat/your-task-description
```

`--force-with-lease` is acceptable **only** on your own task branch. Never force-push `main`, and never rewrite a branch another contributor is working on.

### Resolving conflicts safely

1. Run `git status` to list the conflicted files.
2. Open each file and locate the conflict markers:

   ```text
   <<<<<<< HEAD
   changes already on your branch
   =======
   changes coming from main
   >>>>>>> main
   ```

3. Edit the file so that both sets of changes are integrated correctly, then delete all marker lines.
4. Stage the resolved files:

   ```bash
   git add <resolved-files>
   ```

5. Finish the operation:
   - After a merge: `git commit` (a merge commit is created).
   - After a rebase: `git rebase --continue`.
6. **Re-run the relevant tests** to confirm the resolution did not break anything.
7. Push the branch and request a new review — your previous approval was dismissed by the push.

If the conflict becomes unmanageable, abort and start over rather than committing a partial resolution:

```bash
git merge --abort     # or: git rebase --abort
```

Do not resolve conflicts by deleting code you do not understand. When in doubt, ask the author of the incoming change.

---

## 7. Security and repository hygiene

- **Never commit secrets.** This includes passwords, API keys, access tokens, certificates, and `.env` files. Copy [.env.example](.env.example) to `.env` locally and keep `.env` untracked.
- **Never commit database files** (`*.db`, `*.sqlite`, `*.sqlite3`) or generated data. Only curated fixtures under `data/samples/` belong in Git; keep large or generated datasets in `data/raw/` or `data/processed/` on your machine.
- **Avoid unnecessary generated files and large binaries.** Do not add build output, caches, logs, archives, or documents that are not part of the deliverable.
- **Do not add editor, OS, or virtual-environment files** (`.venv/`, `.vscode/`, `.idea/`, `.DS_Store`). They are already listed in `.gitignore`.
- **Check what you are staging** before every commit:

  ```bash
  git status --short
  git diff --cached --stat
  ```

If a secret is committed by mistake, revoke or rotate it immediately and notify the maintainers. Deleting it in a later commit does not remove it from the repository history.

---

## 8. Related documentation

| Document | Purpose |
| :--- | :--- |
| [docs/project-overview.md](docs/project-overview.md) | Problem context, scope, and objectives |
| [docs/architecture.md](docs/architecture.md) | Components, data flow, and technology stack |
| [docs/api-contract.md](docs/api-contract.md) | Request/response contracts between frontend and backend |
| [docs/mathematical-model.md](docs/mathematical-model.md) | MILP formulation and constraint definitions |
| [docs/data-dictionary.md](docs/data-dictionary.md) | Dataset schemas and field definitions |
| [docs/testing-strategy.md](docs/testing-strategy.md) | Test tiers, invariants, and required edge cases |
| [.github/pull_request_template.md](.github/pull_request_template.md) | Required PR structure |
| [data/README.md](data/README.md) | Dataset tracking policy |
