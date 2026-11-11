# CLAUDE.md — Agent & Contributor Technical Guidelines

This document provides explicit guidelines and constraints for Claude Code, AI
coding assistants, and contributors interacting with the **LogiMind** repository.

---

## 1. Prime Directives

1. **Read Before Writing:** Always consult `README.md`, `docs/`, and existing
   module contracts before introducing code or modifying data structures.
2. **Do Not Hallucinate Domain Logic:** Do not invent mathematical constraints,
   business assumptions, or cost matrices. Refer strictly to
   [docs/mathematical-model.md](docs/mathematical-model.md) and confirmed
   Architecture Decision Records (ADRs). **Policy A** is the selected allocation
   policy: one warehouse per order, no split shipments, no unassigned penalty,
   capacity measured in orders, per-SKU inventory, shipping-cost-only objective.
3. **Atomic & Reviewable Changes:** Keep edits small, modular, and easy to review
   in isolation. Avoid bundling multi-role changes in a single operation.
4. **Strict Scope Discipline:** Do not modify files outside the immediate scope
   of the requested task. Do not refactor untouched modules without explicit
   permission.
5. **No Fictional Identity / Deadlines:** Never fabricate GitHub usernames, team
   member identities, deadlines, or fake completion statuses. Use `TBD` until
   validated by human team leads.

---

## 2. Repository Layout & Code Placement

The root directory contains only repository-level files and directories:

```text
.github/        CI, issue templates, PR template
data/           curated fixtures (data/samples/) and future schemas (data/schema/)
docs/           authoritative technical documentation
scripts/        reusable maintenance/generation utilities and the legacy prototype
src/            future Python package (src/logimind/)
tests/          future automated tests
docs/reference/ historical academic source material
docs/decisions/ Architecture Decision Records
docs/project-management/ status, tracker, plans, cleanup record
```

Placement rules:

- **No project source code, datasets, or experimental scripts in the root.**
- Python application code belongs under `src/logimind/` when implementation
  exists: `algorithms/`, `backend/`, `data/`.
- The React frontend is a separate application under `frontend/`; never mix it
  into the Python package.
- Benchmark datasets belong in `data/samples/`; machine-readable schemas belong
  in `data/schema/`.
- Reusable maintenance utilities belong in `scripts/`.
- Automated tests belong in `tests/unit/`, `tests/integration/`, or `tests/e2e/`.
- Technical documentation belongs in `docs/`; ADRs in `docs/decisions/`;
  tracking documents in `docs/project-management/`.
- Do **not** create empty package, frontend, or test directories merely to match
  a planned tree. Create them when they contain real implementation.
- Do **not** add `pyproject.toml` for decoration. Add it when the
  `src/logimind/` package or automated tests actually need packaging/tooling.
- The legacy prototype lives at `scripts/validate_orders.py` with its fixture at
  `data/samples/benchmark_data.json`. It is a demonstration, not Policy A.

---

## 3. Testing & Quality Assurance

1. **Verify Before Reporting:** Only report tests as passing if they have
   actually been executed in the environment.
2. **No Mocked Test Reports:** If runtime dependencies (solver binaries, Node
   modules) are unavailable, explicitly report that tests could not run.
3. **Regression Prevention:** When fixing an issue or implementing a constraint,
   add or update a test under `tests/` to prevent regressions.
4. **Current reality:** No automated test suite exists yet. Do not claim test
   coverage for components that are only planned. The prototype has no
   assertions; CI performs JSON, link, file-presence, and prototype smoke checks.

---

## 4. Git, Security & Safety Controls

1. **No Unauthorized Commits or Pushes:** Do not execute `git commit` or
   `git push` unless the user explicitly instructs you to do so.
2. **Never Push Directly to `main`:** All changes are developed in branch
   namespaces (`feat/`, `fix/`, `docs/`, `test/`, `refactor/`, `chore/`) and
   submitted via Pull Requests.
3. **No Destructive Commands:**
   - NEVER run `git reset --hard` or `git clean -fd`.
   - NEVER force-push (`git push --force` or `--force-with-lease`).
   - NEVER delete existing files or directories without explicit review and
     approval.
   - NEVER delete local or remote branches as part of repository cleanup.
4. **Zero-Secret Tolerance:** Never commit credentials, `.env` files, API keys,
   private certificates, or internal tokens. Always check `.gitignore` before
   adding files.
5. **No Administrative Actions:** Never alter repository access permissions,
   branch protection rules, or merge Pull Requests autonomously.

---

## 5. Code & Commit Conventions

- **Language Policy:**
  - Code, variables, functions, comments, docstrings, schema keys, and git
    commits must be written in **English**.
  - Project documentation may be in English or Vietnamese as specified in the
    documentation index, but code-level artifacts remain English.
- **Naming:**
  - Python files and packages: `snake_case` / lowercase with underscores.
  - Documentation: lowercase-kebab-case (for example
    `docs/project-management/project-status.md`).
  - Configuration files keep the filename required by their tool.
  - Do not rename public API routes, database tables, domain identifiers, or data
    fields merely for filename uniformity.
- **Commit Messages:** Follow Conventional Commits:
  - `feat: <description>`
  - `fix: <description>`
  - `docs: <description>`
  - `test: <description>`
  - `refactor: <description>`
  - `chore: <description>`
- **Formatting:** Comply with `.editorconfig` (LF line endings, UTF-8, 4 spaces
  for Python, 2 spaces for JSON/YAML/JS/Markdown).

---

## 6. Team Boundaries & Documentation Updates

- Do not modify another role's active feature branch or overwrite their work.
- Each topic has one authoritative document:
  - Requirements → `docs/requirements.md`
  - Mathematical model → `docs/mathematical-model.md`
  - API interface → `docs/api-contract.md`
  - Dataset contract → `docs/data-dictionary.md`
  - Testing methodology → `docs/testing-strategy.md`
  - Architecture → `docs/architecture.md`
  - Project status → `docs/project-management/project-status.md`
- Other documents must link to these instead of duplicating their content.
- When moving or renaming a file, update every import, relative path, Markdown
  link, CI reference, and command example in the same change.
- Keep internal Markdown links valid; CI checks them.

---

## 7. File Cleanup Rules

- Do not keep duplicate data dictionaries or competing contracts; consolidate
  into the authoritative document and leave a pointer only if needed.
- Do not keep root-level scripts, datasets, or academic binaries; move them to
  `scripts/`, `data/samples/`, or `docs/reference/` with clear documentation.
- Archived/reference material must have an explicit reason; do not create a
  dumping-ground `archive/` directory.
- Preserve academic source material and curated fixtures. When uncertain, keep or
  archive rather than delete.
- Do not commit generated caches, virtual environments, databases, logs, or build
  output. `.gitignore` already covers these.
