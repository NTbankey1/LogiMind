# Changelog

All notable changes to the **LogiMind** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Initial project scaffolding and repository hygiene configuration (`.gitignore`, `.editorconfig`, `.gitattributes`, `.env.example`).
- Comprehensive documentation architecture (`docs/`):
  - Project Overview and Requirements (`project-overview.md`, `requirements.md`).
  - Mathematical model specification blueprint (`mathematical-model.md`).
  - System architecture and data flow diagrams (`architecture.md`).
  - Standardized API contract and schemas (`api-contract.md`).
  - Data dictionary and field schemas (`docs/data-dictionary.md`).
  - Testing strategy and integration guidelines (`testing-strategy.md`, `integration-guide.md`).
  - Team responsibilities matrix and progress tracker (`team-responsibilities.md`).
  - Git branching and contribution workflow (`git-workflow.md`, `CONTRIBUTING.md`).
  - Architecture Decision Records index and template (`docs/decisions/`).
- GitHub workflow automation:
  - CI workflow (`.github/workflows/ci.yml`) for repository hygiene and markdown integrity.
  - Pull Request template (`.github/pull_request_template.md`).
  - Issue templates for bug reports, feature requests, and tasks (`.github/ISSUE_TEMPLATE/`).
- Module placeholder READMEs (`src/`, `tests/`, `data/`, `scripts/`).

### Changed
- Reorganized the repository layout:
  - Academic analysis document moved to `docs/reference/project-analysis.docx`.
  - Legacy prototype moved to `scripts/validate_orders.py` with `__file__`-relative data resolution and an optional dataset argument.
  - Prototype fixture moved to `data/samples/benchmark_data.json`.
  - Duplicate root `data-dictionary.md` consolidated into `docs/data-dictionary.md` as Appendix A.
  - Project-management documents renamed to lowercase-kebab-case.
- Updated README, CLAUDE.md, CONTRIBUTING.md, documentation links, architecture paths, and CI to the new layout.
- Added a CI smoke check that runs the legacy allocation prototype.

---

## [0.1.0] - 2026-10-29
- Initial repository setup and baseline documentation release.
