# ADR-001: Choice of Optimization Solver Library

## Status
PROPOSED

## Context
LogiMind requires an LP/MILP optimization solver engine in Python to solve multi-warehouse order allocations. The solver must run reliably on developer laptops without requiring expensive commercial licenses (such as Gurobi or CPLEX) while remaining easy to install and teach in an academic context.

## Options Considered
1. **PuLP (Coin-OR CBC Backend):**
   - *Pros:* Simple, expressive Pythonic formulation; bundled with default CBC solver; standard teaching tool in operations research courses; zero licensing barrier.
   - *Cons:* Slower execution on very large-scale integer programs (> 100,000 variables).
2. **Google OR-Tools:**
   - *Pros:* High performance C++ backend with Python bindings; supports CP-SAT and GLOP/CBC solvers; handles larger combinatorial problems.
   - *Cons:* Slightly steeper learning curve for student modeling; syntax differs from classical algebraic modeling.
3. **SciPy (`scipy.optimize.milp`):**
   - *Pros:* Standard scientific Python distribution using HiGHS solver backend.
   - *Cons:* Lower-level matrix-based constraint entry; less intuitive for algebraic index formulation.

## Decision (Proposed)
Adopt **PuLP** with CBC backend as the primary modeling library for TV3's initial baseline and MILP formulation, with an architectural adapter allowing swapping to Google OR-Tools if scaling issues arise.

## Consequences
- **Positive:** Low barrier to entry for TV1 and TV3; clear readability in academic reports.
- **Negative / Risks:** Benchmarks with more than 10,000 orders may require tuning solve time limits.
