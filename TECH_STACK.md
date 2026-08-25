# Technology Stack Specification — HOSPITALITY

## 1. Architecture Tiers

### Client / Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript 5.0+
- **Styling**: Tailwind CSS 3.4+ / Custom Healthcare UI System (`#005EB8` primary)
- **Icons**: Lucide React
- **Visualizations**: Recharts
- **UX Paradigm**: Single-Page Application (SPA) with smooth section scrolling and reactive state management

### Backend & API
- **Framework**: FastAPI (Async Python 3.11+)
- **ORM & Database**: SQLAlchemy 2.0 (Async) + `aiosqlite` (SQLite default) / `asyncpg` (PostgreSQL ready)
- **Data Validation & Serialization**: Pydantic v2
- **Document Processing**: `pdfplumber`, `PyPDF2`
- **Testing**: `pytest`, `pytest-asyncio`

### Interoperability & Standards
- **Health Standards**: HL7 FHIR R4, ABDM HFR Unique ID (`IN...`), NHCX Electronic Claims Specifications
- **Data Provenance**: Multi-tier confidence tagging (`AUTHORITATIVE`, `PUBLIC_VERIFIED`, `SIMULATED`)
