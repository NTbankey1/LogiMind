# LogiMind Documentation Center

Welcome to the technical and architectural documentation index for the **LogiMind** multi-warehouse order allocation system.

---

## 1. Document Directory

| Document | Primary Owner | Description |
| :--- | :--- | :--- |
| [Project Overview](project-overview.md) | All Members | Problem background, domain analysis, business objectives, and scope limits. |
| [Requirements](requirements.md) | TV1 & TV6 | Functional (FR) and Non-Functional (NFR) requirements specification. |
| [Mathematical Model](mathematical-model.md) | TV1 | Sets, parameters, decision variables, constraints, objective function, and examples. |
| [Architecture](architecture.md) | TV5 & Tech Lead | System architecture, component communication, tech stack roadmap, and flow diagrams. |
| [API Contract](api-contract.md) | TV4 & TV5 | Policy A request/response schemas, status semantics, validation rules, and error codes. |
| [Data Dictionary](data-dictionary.md) | TV2 | Entity definitions, field types, constraints, and the legacy prototype appendix. |
| [Testing Strategy](testing-strategy.md) | TV6 | Testing tiers, coverage expectations, edge cases, and automated validation. |
| [Integration Guide](integration-guide.md) | TV6 & Tech Lead | Hand-off checklists, cross-module dependencies, and milestone synchronization. |
| [Team Responsibilities](team-responsibilities.md) | All Members | Detailed roles (TV1–TV6), deliverables, dependencies, and completion criteria. |
| [Git Workflow](git-workflow.md) | Tech Lead | Branching model, PR process, commit conventions, and conflict resolution. |
| [Architecture Decisions (ADRs)](decisions/README.md) | All Members | Records of significant architectural and technology selection decisions. |

### Project management and reference

| Document | Description |
| :--- | :--- |
| [Project Status](project-management/project-status.md) | Evidence-based status of TV1–TV6, blockers, risks, and verification evidence. |
| [Task Tracker](project-management/task-tracker.md) | Task checklist and dependency matrix. |
| [Test Plan](project-management/test-plan.md) | Test tiers, edge cases, and execution status. |
| [Integration Plan](project-management/integration-plan.md) | Milestones and cross-module synchronization plan. |
| [Repository Cleanup Plan](project-management/repository-cleanup-plan.md) | Audit, file classifications, target layout, and verification for the repository cleanup. |
| [Project Analysis (DOCX)](reference/project-analysis.docx) | Original Vietnamese academic analysis and business source material. |

---

## 2. Reading Roadmap for Roles

- **Mathematical Modeler (TV1):** Start at [Mathematical Model](mathematical-model.md) and [Requirements](requirements.md).
- **Data Engineer (TV2):** Start at [Data Dictionary](data-dictionary.md) and [Testing Strategy](testing-strategy.md).
- **Algorithm Engineer (TV3):** Start at [Mathematical Model](mathematical-model.md), [Data Dictionary](data-dictionary.md), and [API Contract](api-contract.md).
- **Frontend Engineer (TV4):** Start at [API Contract](api-contract.md) and [Architecture](architecture.md).
- **Backend Engineer (TV5):** Start at [Architecture](architecture.md), [API Contract](api-contract.md), and [Data Dictionary](data-dictionary.md).
- **QA & Integration Lead (TV6):** Start at [Testing Strategy](testing-strategy.md), [Integration Guide](integration-guide.md), and [Requirements](requirements.md).
