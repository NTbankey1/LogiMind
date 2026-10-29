# Architecture Decision Records (ADRs)

This directory contains records of significant technical and architectural decisions made by the **LogiMind** team.

---

## 1. What is an ADR?

An Architecture Decision Record (ADR) captures an important architectural decision made along with its context, options considered, and consequences.

---

## 2. ADR Statuses
- **PROPOSED:** Under team review and evaluation.
- **ACCEPTED:** Confirmed and adopted by the team.
- **REJECTED:** Considered but not selected.
- **SUPERSEDED:** Replaced by a subsequent ADR.

---

## 3. ADR Index

| ADR ID | Title | Date | Status | Primary Decision Owner |
| :--- | :--- | :--- | :--- | :--- |
| [ADR-001](0001-choice-of-optimization-solver-library.md) | Choice of Optimization Solver Library (PuLP vs. OR-Tools) | 2026-10-29 | PROPOSED | TV3 & TV1 |
| [ADR-002](0002-choice-of-backend-framework.md) | Choice of Backend API Framework (FastAPI) | 2026-10-29 | PROPOSED | TV5 |
| [ADR-003](0003-choice-of-database-engine.md) | Choice of Local Persistence Database (SQLite) | 2026-10-29 | PROPOSED | TV5 |

---

## 4. ADR Template

To create a new ADR, copy the following structure into `docs/decisions/XXXX-short-title.md`:

```markdown
# ADR-XXXX: [Short Title]

## Status
[PROPOSED | ACCEPTED | REJECTED | SUPERSEDED]

## Context
What is the problem or architectural question we are trying to solve? What are the constraints?

## Options Considered
1. **Option A:** [Pros & Cons]
2. **Option B:** [Pros & Cons]

## Decision
Which option did we select and why?

## Consequences
- **Positive:** What benefits do we gain?
- **Negative / Risks:** What trade-offs or technical debt do we accept?
```
