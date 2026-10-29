# Contributing to LogiMind

Thank you for contributing to the **LogiMind** project! This repository serves as our team collaboration hub. To maintain code quality, avoid merge conflicts, and ensure smooth integration across all 6 roles, please adhere strictly to these guidelines.

---

## 1. Team Collaboration Principles

- **No Direct Commits to `main`:** The `main` branch is protected and contains reviewed, deployable artifacts.
- **Task-Based Branches:** Branches are created per feature or task, **not** per team member. Multiple members can collaborate cleanly through distinct task branches.
- **Contract-First Development:** Agree on interfaces ([docs/api-contract.md](docs/api-contract.md), [docs/mathematical-model.md](docs/mathematical-model.md), [docs/data-dictionary.md](docs/data-dictionary.md)) before implementing dependent modules.

---

## 2. Branching Conventions

Use clear branch prefixes followed by a brief, kebab-case task description:

| Branch Prefix | Purpose | Example |
| :--- | :--- | :--- |
| `docs/` | Documentation additions or updates | `docs/math-model-constraints` |
| `feat/` | New functional features or modules | `feat/milp-solver-baseline` |
| `fix/` | Bug fixes and constraint corrections | `fix/inventory-overflow-check` |
| `test/` | Test suites, test data, and fixtures | `test/add-split-shipment-cases` |
| `chore/` | Tooling, CI, dependencies, housekeeping | `chore/setup-ruff-linter` |

---

## 3. Standard 10-Step Workflow

1. **Synchronize Base Branch:**
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Create a Dedicated Task Branch:**
   ```bash
   git checkout -b feat/your-task-description
   ```
3. **Make Atomic Changes:** Work within your assigned module boundary. Avoid touching unrelated files.
4. **Run Local Checks & Tests:**
   - Verify code formatting and linting.
   - Run relevant unit/integration tests and verify they pass.
5. **Stage & Commit Using Conventional Commits:**
   ```bash
   git add <modified-files>
   git commit -m "feat: implement warehouse capacity constraint check"
   ```
6. **Push Branch to GitHub:**
   ```bash
   git push -u origin feat/your-task-description
   ```
7. **Open a Pull Request (PR):**
   - Target base: `main`
   - Fill out the PR template thoroughly.
   - Link related issue or task ID.
8. **Code Review & Automated CI:**
   - At least one team member must review the PR.
   - Automated CI checks must pass.
9. **Merge Pull Request:**
   - Use "Squash and merge" or "Rebase and merge" based on team consensus to keep a clean history.
10. **Clean Up Branch:**
    - Delete the remote and local branch after merge.

---

## 4. Conventional Commit Standards

Every commit message must follow the Conventional Commits format:

```text
<type>(<optional scope>): <short description in imperative mood>

[optional body explaining motivation and technical context]

[optional footer(s), e.g., Closes #12]
```

### Supported Types:
- `feat`: A new feature (e.g., `feat: add greedy heuristic solver`)
- `fix`: A bug fix (e.g., `fix: correct index mapping in decision variable`)
- `docs`: Documentation only changes (e.g., `docs: clarify objective penalties`)
- `test`: Adding or updating tests (e.g., `test: add infeasible order fixture`)
- `chore`: Maintenance, dependencies, configs (e.g., `chore: update ignore rules`)
- `refactor`: Code change that neither fixes a bug nor adds a feature

---

## 5. Keeping Your Branch Up to Date & Resolving Merge Conflicts

When `main` has progressed while you are working on your branch:

### Step 1: Fetch and Rebase or Merge
```bash
git checkout main
git pull origin main
git checkout feat/your-task-description
git merge main
# Or alternatively, rebase if agreed upon:
# git rebase main
```

### Step 2: Resolving Conflicts Safely
1. Inspect conflicting files indicated by Git.
2. Edit conflicting files, keeping desired changes and removing conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
3. Run test suites to ensure resolution did not introduce regression.
4. Stage resolved files:
   ```bash
   git add <resolved-files>
   git commit -m "chore: resolve merge conflict with main"
   ```
5. Push updated branch to remote:
   ```bash
   git push origin feat/your-task-description
   ```

---

## 6. Security & Hygiene Checklist

- [ ] No `.env`, secret keys, or local credentials committed.
- [ ] No local database files (`*.sqlite`, `*.db`) committed.
- [ ] No OS junk (`.DS_Store`, `Thumbs.db`) or IDE configuration files committed.
- [ ] Code is formatted according to `.editorconfig`.
