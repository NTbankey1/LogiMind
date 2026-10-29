# CLAUDE.md — Agent & Contributor Technical Guidelines

This document provides explicit guidelines and constraints for Claude Code, AI coding assistants, and contributors interacting with the **LogiMind** repository.

---

## 1. Prime Directives

1. **Read Before Writing:** Always consult `README.md`, `docs/`, and existing module contracts before introducing code or modifying data structures.
2. **Do Not Hallucinate Domain Logic:** Do not invent mathematical constraints, business assumptions, or cost matrices. Refer strictly to [docs/mathematical-model.md](docs/mathematical-model.md) and confirmed Architecture Decision Records (ADRs).
3. **Atomic & Reviewable Changes:** Keep edits small, modular, and easy to review in isolation. Avoid bundling multi-role changes in a single operation.
4. **Strict Scope Discipline:** Do not modify files outside the immediate scope of the requested task. Do not refactor untouched modules without explicit permission.
5. **No Fictional Identity / Deadlines:** Never fabricate GitHub usernames, team member identities, deadlines, or fake completion statuses. Use `TBD` until validated by human team leads.

---

## 2. Testing & Quality Assurance

1. **Verify Before Reporting:** Only report tests as passing if they have actually been executed and verified in the environment.
2. **No Mocked Test Reports:** If runtime dependencies (e.g., Python solver binaries, Node modules) are unavailable, explicitly report that tests could not be executed due to missing environment components.
3. **Regression Prevention:** When fixing an issue or implementing a constraint, add or update a test case in `tests/` to prevent regressions.

---

## 3. Git, Security & Safety Controls

1. **No Unauthorized Commits or Pushes:** Do not execute `git commit` or `git push` unless the user explicitly instructs you to do so.
2. **Never Push Directly to `main`:** All code and documentation changes must be developed in branch namespaces (`feat/`, `fix/`, `docs/`, `test/`, `chore/`) and submitted via Pull Requests.
3. **No Destructive Commands:**
   - NEVER run `git reset --hard` or `git clean -fd`.
   - NEVER force-push (`git push --force` or `--force-with-lease`).
   - NEVER delete existing files or directories without explicit review and approval.
4. **Zero-Secret Tolerance:** Never commit credentials, `.env` files, API keys, private certificates, or internal tokens. Always check `.gitignore` before adding files.
5. **No Administrative Actions:** Never attempt to alter repository access permissions, branch protection rules, or merge Pull Requests autonomously.

---

## 4. Code & Commit Conventions

- **Language Policy:**
  - Code, variables, functions, comments, docstrings, schema keys, and git commits must be written in **English**.
  - Project documentation may be in English or Vietnamese as specified in the respective doc index, but code-level artifacts remain English.
- **Commit Messages:** Follow Conventional Commits format:
  - `feat: <description>`
  - `fix: <description>`
  - `docs: <description>`
  - `test: <description>`
  - `chore: <description>`
- **Formatting:** Comply with `.editorconfig` (LF line endings, UTF-8, 4 spaces for Python, 2 spaces for JSON/YAML/JS/Markdown).
