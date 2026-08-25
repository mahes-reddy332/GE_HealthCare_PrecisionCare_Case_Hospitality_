# REST API Specification — HOSPITALITY

**Base URL**: `http://localhost:8000/api/v1`  
**Protocol**: REST / JSON  
**Specification**: OpenAPI 3.1 (Swagger interactive docs at `/docs`)

---

## 📡 Endpoints

### 1. Hospital Discovery & Infrastructure
- `GET /api/v1/hospitals`: Filter hospitals by city, district, specialty, scheme/insurer, and geo-radius (`lat`, `lon`, `radius_km`).
- `GET /api/v1/hospitals/{id}`: Detailed hospital profile including facility identifiers (HFR, ROHINI), operational specialties, and accreditation.
- `GET /api/v1/hospitals/{id}/rooms`: List room categories (General, Semi-Private, Private, ICU) with daily tariffs and provenance tags.
- `GET /api/v1/hospitals/{id}/beds`: Live bed availability inventory by room category.
- `GET /api/v1/hospitals/{id}/schemes`: List of empaneled private insurers and government schemes.

### 2. Policy Ingestion & Extraction
- `POST /api/v1/policies/upload`: Upload policy PDF for OCR and structured AI extraction.
- `POST /api/v1/policies/manual`: Submit structured insurance parameters directly.
- `POST /api/v1/policies/mock`: Generate realistic mock policies (Star Health, HDFC ERGO, PM-JAY, Arogya Karnataka) for instant demo testing.
- `GET /api/v1/policies/{id}`: Retrieve stored policy clauses, sublimits, and extraction confidence.

### 3. Matching & Cost Intelligence
- `POST /api/v1/matching/hospitals`: Multi-criteria search returning scored, ranked hospitals based on active policy terms and user location.
- `POST /api/v1/matching/deduction-simulate`: Calculate exact out-of-pocket share and proportionate deduction penalty for a specific hospital, procedure, and room type.

### 4. Care Journey State Machine
- `GET /api/v1/patients/{id}/journey`: Retrieve active care journey stage and event timeline.
- `POST /api/v1/patients/{id}/journey/events`: Record milestone events (`PRE_AUTH_SUBMITTED`, `ROOM_ALLOCATED`, `DISCHARGE_BILL_GENERATED`).

### 5. System Provenance & Health
- `GET /api/v1/data-sources`: List all data providers, sync timestamps, and authoritative reliability metrics.
- `GET /api/v1/health`: System health check and database connectivity status.
