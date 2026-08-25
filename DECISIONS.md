# Architecture Decision Records (ADRs) — HOSPITALITY

## ADR-001: Separation of LLM Natural Language Processing and Mathematical Calculation
- **Status**: Accepted
- **Context**: LLMs cannot be trusted to perform accurate, deterministic multi-step arithmetic for health insurance deductibles, room rent penalties, and copayments.
- **Decision**: The LLM is used exclusively for extracting structured JSON constraints from policy documents. All financial and deduction calculations are executed by a pure, tested Python rule engine.
- **Consequence**: Zero mathematical hallucinations in financial figures shown to users.

## ADR-002: Dual Database Strategy (SQLite for Portable Demo, PostgreSQL Ready)
- **Status**: Accepted
- **Context**: Hackathon evaluations require instant zero-friction local execution without requiring external database server setup.
- **Decision**: Use `aiosqlite` with async SQLAlchemy 2.0 as the out-of-the-box default, designed with standard relational types that seamlessly switch to `asyncpg` PostgreSQL via `.env`.
- **Consequence**: Guaranteed local reproducibility with immediate enterprise upgrade path.

## ADR-003: Transparent Provenance & Simulated Data Tagging
- **Status**: Accepted
- **Context**: Certain national data (real-time bed availability, private insurer empanelment APIs) does not exist publicly.
- **Decision**: Generate realistic synthetic data for missing dimensions, but explicitly tag all such records with `data_status: SIMULATED` and render distinctive badges on the UI.
- **Consequence**: Absolute transparency with judges and evaluators regarding real vs synthetic inputs.
