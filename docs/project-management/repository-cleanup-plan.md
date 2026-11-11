# Repository Architecture Refactoring & Cleanup Plan

> **Status:** Implemented on `refactor/repository-structure-cleanup` (pending PR review)
> **Baseline commit:** `fb15ef2` on `origin/main`
> **Scope:** Repository organization only. No change to the Policy A mathematical
> model, solver behavior, or canonical data semantics.

---

## 1. Why the old structure was difficult to maintain

The baseline had 41 tracked files and placed four unrelated artifacts in the
repository root:

- `validate_orders.py` — the only executable prototype, but mixed with
  repository-level files.
- `benchmark_data.json` — a dataset in the root instead of `data/samples/`.
- `data-dictionary.md` — a duplicate dictionary that conflicted with
  `docs/data-dictionary.md`.
- `LogiMind_phantich.docx` — an academic source document in the root.

Project-management filenames used inconsistent UPPER_SNAKE_CASE, and the `src/`,
`scripts/`, and `tests/` READMEs described planned structures that no longer
matched the intended package layout (`src/logimind/`, separate `frontend/`).
Readers could not tell which data dictionary was authoritative, and execution
instructions depended on the current working directory.

The cleanup preserves all content and Git history while giving each artifact one
clear location.

---

## 2. Complete inventory and classification

Every tracked file at the baseline receives exactly one classification:

- **KEEP** — stays in its current location (content may be updated).
- **MOVE** — relocated or renamed.
- **MERGE** — content consolidated into another authoritative file.
- **ARCHIVE** — historical/academic material preserved under `docs/reference/`.
- **DELETE** — removed with no remaining purpose. **None.**

| # | File path (baseline) | Action | New path / disposition | Reason | References updated | Verification |
|---:|---|---|---|---|---|---|
| 1 | `.editorconfig` | KEEP | — | Formatting standard (LF, UTF-8, indentation). | No | Inspected |
| 2 | `.env.example` | KEEP | — | Environment template; no secrets. | No | Inspected |
| 3 | `.gitattributes` | KEEP | — | LF normalization and diff attributes. | No | Inspected |
| 4 | `.github/ISSUE_TEMPLATE/bug_report.md` | KEEP | — | GitHub issue template. | No | Link check |
| 5 | `.github/ISSUE_TEMPLATE/feature_request.md` | KEEP | — | GitHub issue template. | No | Link check |
| 6 | `.github/ISSUE_TEMPLATE/task.md` | KEEP | — | GitHub task template. | No | Link check |
| 7 | `.github/pull_request_template.md` | KEEP | — | PR review checklist. | No | Link check |
| 8 | `.github/workflows/ci.yml` | KEEP | — | CI hygiene pipeline; extended with a prototype smoke step. | Yes (smoke step) | YAML parse + local run |
| 9 | `.gitignore` | KEEP | — | Covers caches, venvs, Node, SQLite, logs, IDE files; curated samples remain trackable. | No | `git status` |
| 10 | `CHANGELOG.md` | KEEP | — | Release history; Unreleased section updated with the cleanup. | Yes | Link check |
| 11 | `CLAUDE.md` | KEEP | — | Agent/contributor rules; rewritten for the new layout and cleanup boundaries. | Yes | Review |
| 12 | `CONTRIBUTING.md` | KEEP | — | Git workflow; commands updated for moved prototype/fixtures. | Yes | Command test |
| 13 | `LogiMind_phantich.docx` | ARCHIVE | `docs/reference/project-analysis.docx` | Academic source document; preserve but separate from active development. | Yes (`README`, project status, docs index) | SHA-256 unchanged |
| 14 | `README.md` | KEEP | — | Root entry point; rewritten for the cleaned layout and honest status. | Yes | Link check |
| 15 | `benchmark_data.json` | MOVE | `data/samples/benchmark_data.json` | Dataset belongs with curated fixtures; documented as legacy prototype input. | Yes (`scripts/validate_orders.py`, docs) | JSON parse + prototype run |
| 16 | `data-dictionary.md` | MERGE | Merged into `docs/data-dictionary.md` as Appendix A; root file removed | Duplicate dictionary; prototype schema preserved in the authoritative document. | Yes (README, index, project docs) | Link check; zero root refs |
| 17 | `data/README.md` | KEEP | — | Dataset policy; rewritten with the actual catalogue and legacy status. | Yes | Link check |
| 18 | `data/samples/sample_small.json` | KEEP | — | Curated draft fixture; content unchanged (replacement is TV2 work). | No | JSON parse |
| 19 | `docs/api-contract.md` | KEEP | — | Proposed API contract; still contains pre-Policy-A split fields. | No (flagged follow-up) | Link check |
| 20 | `docs/architecture.md` | KEEP | — | Proposed architecture; paths/status updated and split-shipment output wording removed. | Yes | Link check |
| 21 | `docs/data-dictionary.md` | KEEP | — | Authoritative dictionary; receives legacy prototype Appendix A and Policy A boundary note. | Yes | Link check |
| 22 | `docs/decisions/0001-choice-of-optimization-solver-library.md` | KEEP | — | ADR-001 (proposed). | No | Link check |
| 23 | `docs/decisions/0002-choice-of-backend-framework.md` | KEEP | — | ADR-002 (proposed). | No | Link check |
| 24 | `docs/decisions/0003-choice-of-database-engine.md` | KEEP | — | ADR-003 (proposed). | No | Link check |
| 25 | `docs/decisions/README.md` | KEEP | — | ADR index and template. | No | Link check |
| 26 | `docs/git-workflow.md` | KEEP | — | Branch/PR examples updated to current paths and Policy A terminology. | Yes | Link check |
| 27 | `docs/index.md` | KEEP | — | Documentation centre; project-management and reference links added. | Yes | Link check |
| 28 | `docs/integration-guide.md` | KEEP | — | Handoff checklists; module paths and Policy A wording updated. | Yes | Link check |
| 29 | `docs/mathematical-model.md` | KEEP | — | Policy A formulation; content unchanged, line endings normalized to LF. | No | Content equality check |
| 30 | `docs/project-management/INTEGRATION_PLAN.md` | MOVE | `docs/project-management/integration-plan.md` | Lowercase-kebab naming; paths updated. | Yes | Link check |
| 31 | `docs/project-management/PROJECT_STATUS.md` | MOVE | `docs/project-management/project-status.md` | Lowercase-kebab naming; evidence paths updated. | Yes | Link check |
| 32 | `docs/project-management/TASK_TRACKER.md` | MOVE | `docs/project-management/task-tracker.md` | Lowercase-kebab naming; links updated. | Yes | Link check |
| 33 | `docs/project-management/TEST_PLAN.md` | MOVE | `docs/project-management/test-plan.md` | Lowercase-kebab naming; commands/paths updated. | Yes | Link check |
| 34 | `docs/project-overview.md` | KEEP | — | Business context; still mentions split-shipment scope (flagged follow-up). | No | Link check |
| 35 | `docs/requirements.md` | KEEP | — | Policy A requirements; content unchanged, line endings normalized to LF. | No | Content equality check |
| 36 | `docs/team-responsibilities.md` | KEEP | — | Role matrix; planned paths and two Policy A wording points updated. | Yes | Link check |
| 37 | `docs/testing-strategy.md` | KEEP | — | Test strategy; still describes EDGE-03 split trade-off (flagged follow-up). | No | Link check |
| 38 | `scripts/README.md` | KEEP | — | Rewritten: documents the actual prototype and planned TV2 tooling. | Yes | Link check |
| 39 | `src/README.md` | KEEP | — | Rewritten: intended `src/logimind/` layout and separation from `frontend/`. | Yes | Link check |
| 40 | `tests/README.md` | KEEP | — | Rewritten: states no tests exist and documents the intended layout. | Yes | Link check |
| 41 | `validate_orders.py` | MOVE | `scripts/validate_orders.py` | Prototype belongs in `scripts/`; default input resolved from `__file__`; optional path argument; CI smoke check added. | Yes (`CONTRIBUTING`, README, PM docs) | Runs from root and `scripts/` |

**New file:** `docs/project-management/repository-cleanup-plan.md` (this record).

### Cleanup summary

| Action | Count | Details |
|---|---:|---|
| Kept | 33 | 41 baseline files minus 1 archived, 1 merged, 6 moved |
| Moved | 6 | `benchmark_data.json`, `validate_orders.py`, and four project-management document renames |
| Merged | 1 | Root `data-dictionary.md` → `docs/data-dictionary.md` Appendix A |
| Archived | 1 | `LogiMind_phantich.docx` → `docs/reference/project-analysis.docx` |
| Deleted | 0 | No file was discarded |

---

## 3. Detailed decisions for key assets

### 3.1 Duplicate data dictionaries

- **Finding:** The root dictionary documented only the prototype's flat schema;
  `docs/data-dictionary.md` described a broader proposed relational schema.
- **Decision:** `docs/data-dictionary.md` is authoritative. The prototype schema
  is preserved as **Appendix A**, including its limitations. The root file is
  removed after every reference is updated.
- **Policy boundary:** A notice at the top states that Policy A is the selected
  policy and that the tables are a proposed storage schema, not the canonical
  benchmark contract. Fields outside the Policy A objective are explicitly
  flagged. TV2 still owns the canonical Policy A schema.

### 3.2 Root-level prototype

- **Finding:** `validate_orders.py` and `benchmark_data.json` are the only
  executable baseline and must not be deleted.
- **Decision:** Move to `scripts/validate_orders.py` and
  `data/samples/benchmark_data.json`. The script resolves its default input
  relative to the repository and accepts an optional path, so it works from any
  working directory. CI runs it as a smoke check.
- **Status:** Still a nearest-warehouse demonstration, **not** Policy A. This is
  stated in the README, scripts README, data README, and dictionary Appendix A.

### 3.3 Project analysis document

- **Finding:** Original Vietnamese academic analysis and business source
  material. Disposable status not established.
- **Decision:** Archive under `docs/reference/project-analysis.docx`; binary
  SHA-256 verified unchanged before/after the move. References in the README,
  documentation index, and project status updated.

### 3.4 Placeholder READMEs

- `src/README.md` now describes only the intended `src/logimind/` layout and
  explicitly forbids fake packages.
- `scripts/README.md` documents the real prototype and the planned TV2 tooling.
- `tests/README.md` states clearly that no automated tests exist.
- `data/README.md` documents the actual fixture catalogue and legacy status.

### 3.5 Project-management documents

- Kept all four documents and their verification history.
- Renamed to lowercase-kebab-case to match the documentation naming rule:
  `project-status.md`, `task-tracker.md`, `test-plan.md`, `integration-plan.md`.
- Updated every internal link and path; no historical evidence was removed.

### 3.6 `pyproject.toml` deferred

The target direction includes `pyproject.toml`, but the repository currently has
no Python package, tests, or third-party dependencies. Adding one now would be
decoration and would imply tooling that does not exist. It will be added with the
first real package/test code. The README and `src/README.md` record this decision.

---

## 4. Target directory hierarchy (implemented)

```text
LogiMind/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/ci.yml
│   └── pull_request_template.md
├── data/
│   ├── README.md
│   └── samples/
│       ├── benchmark_data.json
│       └── sample_small.json
├── docs/
│   ├── decisions/
│   │   ├── 0001-choice-of-optimization-solver-library.md
│   │   ├── 0002-choice-of-backend-framework.md
│   │   ├── 0003-choice-of-database-engine.md
│   │   └── README.md
│   ├── project-management/
│   │   ├── integration-plan.md
│   │   ├── project-status.md
│   │   ├── repository-cleanup-plan.md
│   │   ├── task-tracker.md
│   │   └── test-plan.md
│   ├── reference/
│   │   └── project-analysis.docx
│   ├── api-contract.md
│   ├── architecture.md
│   ├── data-dictionary.md
│   ├── git-workflow.md
│   ├── index.md
│   ├── integration-guide.md
│   ├── mathematical-model.md
│   ├── project-overview.md
│   ├── requirements.md
│   ├── team-responsibilities.md
│   └── testing-strategy.md
├── scripts/
│   ├── README.md
│   └── validate_orders.py
├── src/
│   └── README.md
├── tests/
│   └── README.md
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CLAUDE.md
├── CONTRIBUTING.md
└── README.md
```

### Deviations from the suggested target tree

- **No `pyproject.toml`** — no package/tests/dependencies yet (see §3.6).
- **No `src/logimind/` package** — no implementation yet; the intended layout is
  documented in `src/README.md`.
- **No `frontend/`** — no frontend application exists.
- **No `tests/unit|integration|e2e` directories** — no tests exist; the intended
  layout is documented in `tests/README.md`.
- **No `data/schema/` yet** — the machine-readable Policy A schema is TV2 work
  and is not in this branch.
- **No `docs/architecture/` or `docs/requirements/` subdirectories** — those
  documents already exist at `docs/` root; creating duplicate directories would
  add clutter.
- **No generic `archive/` directory** — the academic document is in
  `docs/reference/`; legacy executable material remains active in `scripts/` and
  `data/samples/` so it can still be run and tested.

---

## 5. Reference and configuration updates

| Area | Change |
|---|---|
| Root README | Rewritten: status, Policy A, legacy prototype, new tree, commands, docs links, team roles, limitations. |
| CLAUDE.md | Added layout/placement rules, testing reality, `refactor/` commits, team boundaries, cleanup rules. |
| CONTRIBUTING.md | Prototype and fixture commands updated to new paths. |
| docs/index.md | Project-management and reference entries added; data dictionary description updated. |
| docs/architecture.md | Status banner, planned repository mapping, corrected frontend ADR status, removed split-shipment output wording. |
| docs/team-responsibilities.md | Planned module paths updated; two Policy A wording corrections. |
| docs/integration-guide.md | Planned module/test paths updated; Policy A constraint wording. |
| docs/git-workflow.md | Example paths updated; split-penalty example replaced. |
| Project-management docs | Renamed; links, fixture paths, prototype locations, and dictionary references updated. |
| data/README.md | Actual catalogue, legacy status, JSON/prototype commands, tracking rules. |
| scripts/README.md | Real prototype usage and exit codes; planned TV2 tooling. |
| src/README.md, tests/README.md | Intended layout only; no fake components. |
| CHANGELOG.md | Unreleased entry records the reorganization. |
| CI | Added `python scripts/validate_orders.py` smoke step; JSON loop now covers both fixtures automatically. |
| `.gitignore`, `.editorconfig`, `.gitattributes`, `.env.example` | Unchanged; already correct for the new layout. |

---

## 6. Verification protocol and results

Commands executed from the repository root after the final changes (results are
also recorded in the Pull Request):

| Check | Result |
|---|---|
| `git status --short` | Only intended cleanup changes; no untracked artifacts after commit |
| `git diff --check` | No whitespace errors |
| `python -m json.tool data/samples/*.json` | Both fixtures parse |
| `python scripts/validate_orders.py` (repository root) | Exit `0`; assignments printed |
| `python validate_orders.py` (from `scripts/`) | Exit `0`; path resolution works |
| `python -m py_compile scripts/validate_orders.py` | Exit `0` |
| Internal Markdown link checker | 29 Markdown files checked; 0 broken links |
| Binary integrity (`sha256sum`) | `project-analysis.docx` hash unchanged |
| CI workflow YAML parse | The `repository-hygiene` job and its steps parsed successfully |
| Root acceptance | No scripts, datasets, duplicate dictionary, or academic binary in the root |
| Automated unit tests | **None exist** in the repository; no tests were claimed |

---

## 7. Follow-ups and known limitations

1. **Open TV2 Pull Request #11** is based on `main` and adds the canonical Policy
   A schema, fixtures, generator, validator, and tests. This cleanup branch was
   required to start from `main`, so it retains the draft fixture and proposed
   dictionary. Expect a merge conflict in the data documentation; TV2's canonical
   contract should take precedence when both land.
2. `data/samples/sample_small.json` still contains pre-Policy-A fields. It was
   deliberately not rewritten here; replacing it is TV2 work.
3. `docs/api-contract.md`, `docs/project-overview.md`, and
   `docs/testing-strategy.md` still describe split shipments, penalties, or
   handling costs. These conflicts are already recorded as project blockers
   (B-01/B-03, EDGE-03) and are owned by TV1/TV5/TV6; the cleanup did not rewrite
   those contracts.
4. No solver, backend, database, frontend, or automated test suite exists. The
   intended locations are documented but not scaffolded with fake files.
5. `pyproject.toml` is deferred until actual package/test code exists.
6. `docs/mathematical-model.md` and `docs/requirements.md` were line-ending
   normalized from CRLF to LF per `.gitattributes`; their content is unchanged.
