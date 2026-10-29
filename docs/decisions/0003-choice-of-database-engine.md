# ADR-003: Choice of Local Persistence Database

## Status
PROPOSED

## Context
TV5 needs to store benchmark datasets, warehouse configurations, and historical allocation runs. The database must be easy to run locally across all 6 members' laptops without requiring separate database server administration.

## Options Considered
1. **SQLite:**
   - *Pros:* Zero configuration, file-based, embedded in standard Python (`sqlite3`); no Docker or external database service required; lightweight and completely deterministic.
   - *Cons:* Limited concurrent write throughput (not an issue for single-user evaluation/demo).
2. **PostgreSQL:**
   - *Pros:* Full enterprise relational database features.
   - *Cons:* Requires installing PostgreSQL service or Docker containers on all team laptops, increasing setup hurdles.
3. **In-Memory Mock / JSON Files:**
   - *Pros:* Simplest implementation.
   - *Cons:* Lacks query capabilities, referential integrity, and relational structure.

## Decision (Proposed)
Adopt **SQLite** with SQLAlchemy / SQLModel ORM as the persistence layer for LogiMind.

## Consequences
- **Positive:** Ready out-of-the-box on every OS; single database file (`data/logimind.db` ignored in `.gitignore`).
- **Negative / Risks:** Migration to PostgreSQL in a production cloud environment would require updating connection strings and ORM dialect.
