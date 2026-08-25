# System Architecture — HOSPITALITY

## 1. Overview
HOSPITALITY is a modular, event-driven decision-support platform designed to navigate India's fragmented healthcare financing and hospital delivery system.

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT LAYER                                      |
|  Next.js 14/15 App Router | Tailwind CSS | Recharts | React-Leaflet Map Engine    |
|  - Patient Dashboard  - Policy Uploader  - Cost Comparison  - Care Journey FSM   |
+------------------------------------------+----------------------------------------+
                                           | HTTP / REST (OpenAPI 3.1)
                                           v
+-----------------------------------------------------------------------------------+
|                              API GATEWAY / ROUTER                                 |
|  FastAPI (Async Python 3.11) | Pydantic v2 Serialization | CORS & Rate Limiting   |
+------------------------------------------+----------------------------------------+
                                           |
         +---------------------------------+---------------------------------+
         |                                 |                                 |
         v                                 v                                 v
+------------------+             +-------------------+             +------------------+
| POLICY ENGINE    |             | MATCHING & RULES  |             | DATA HUB         |
| - PDF OCR / Text |             | - Proportionate   |             | - Data.gov.in    |
| - LLM Extraction |             |   Deduction Math  |             | - PM-JAY Master  |
| - Normalized     |             | - Room Rent Capping|             | - CGHS Baselines |
|   FHIR Coverage  |             | - Multi-rank Score|             | - Synthetic Beds |
+------------------+             +-------------------+             +------------------+
         |                                 |                                 |
         +---------------------------------+---------------------------------+
                                           |
                                           v
+-----------------------------------------------------------------------------------+
|                                PERSISTENCE LAYER                                  |
|  SQLAlchemy 2.0 Async ORM | SQLite / PostgreSQL with JSONB Support                |
|  - Hospitals & Specialties     - Room Types & Beds     - Tariffs & Procedures     |
|  - Insurers & Empanelments     - Policies & Clauses    - Care Journey Logs        |
+-----------------------------------------------------------------------------------+
```

## 2. Core Subsystems

### A. Policy Ingestion & Normalization
- Accepts insurer PDF policy certificates, schedules, or manual entry.
- Extracts key insurance parameters: Sum Insured, Cumulative Bonus, Room Rent Limit Type, Room Rent Daily Cap, ICU Cap, Copay Percentage, Disease-Specific Sub-limits, Waiting Periods, and Excluded Consumables.
- Normalizes extracted data into HL7 FHIR `Coverage` and `InsurancePlan` structures.

### B. Ingestion & Provenance Data Hub
- Employs an Abstract Base Provider (`DataProvider`) pattern:
  - `fetch_data()`
  - `normalize()`
  - `validate()`
  - `get_provenance()`
- Every record maintains explicit provenance metadata (`source_id`, `data_status`: `AUTHORITATIVE`, `PUBLIC_VERIFIED`, `SIMULATED`, `confidence`: `HIGH`, `MEDIUM`, `LOW`).

### C. Deterministic Rule & Deduction Engine
- Implements strict IRDAI-compliant health insurance math.
- Never allows LLMs to perform arithmetic on financial figures.
- Calculates exact out-of-pocket penalties when higher room categories are chosen:
  $$\text{Share}_{\text{patient}} = \text{Deductible} + \left(\text{Payable} \times \text{Copay}\right) + \text{Proportionate Penalty} + \text{Non-Payables}$$

### D. Care Journey State Machine
- Manages the 6-stage lifecycle:
  `PRE_ADMISSION` ➔ `ADMISSION` ➔ `INVESTIGATION` ➔ `PROCEDURE` ➔ `RECOVERY` ➔ `DISCHARGE`
- Triggers contextual guidance at each stage (e.g. Pre-auth submission checklist during Admission; Bill audit and non-payable inspection during Discharge).
