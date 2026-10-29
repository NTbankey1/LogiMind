# ADR-002: Choice of Backend API Framework

## Status
PROPOSED

## Context
TV5 needs to build a backend service to orchestrate the solver runs, validate inputs, serve API responses to TV4's frontend, and store allocation records. The backend should integrate seamlessly with Python data science and optimization libraries.

## Options Considered
1. **FastAPI (Python):**
   - *Pros:* Direct in-process execution of Python solver modules (no IPC overhead); automatic OpenAPI/Swagger documentation; fast serialization via Pydantic; async-ready.
   - *Cons:* Requires Python async comprehension, though synchronous endpoint handlers are also supported.
2. **Flask (Python):**
   - *Pros:* Minimalistic, highly familiar to Python beginners.
   - *Cons:* Lacks built-in request schema validation; requires manual Swagger documentation plugins.
3. **Node.js (Express / NestJS):**
   - *Pros:* Unified JavaScript ecosystem with frontend.
   - *Cons:* Would require multi-language IPC (spawning Python child processes or microservices) to invoke the solver, increasing setup complexity for a student project.

## Decision (Proposed)
Adopt **FastAPI** as the backend framework.

## Consequences
- **Positive:** Direct call to TV3 solver classes; automatic interactive docs at `/docs`; strong typing via Pydantic.
- **Negative / Risks:** TV5 must familiarize themselves with FastAPI routing and Pydantic schema validation.
