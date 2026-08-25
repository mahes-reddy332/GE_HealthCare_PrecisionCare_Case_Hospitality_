# Data & Technical Research Log — HOSPITALITY

## Discovery Session 1: Indian Public Health Data Portals
- **Target**: `data.gov.in`, `nhp.gov.in`, MoHFW datasets.
- **Finding**: `data.gov.in` provides downloadable directory datasets containing national healthcare facilities, pincodes, bed capacity estimates, and geo-coordinates.
- **Decision**: Use `data.gov.in` as the foundational authoritative backbone for hospital master data.

## Discovery Session 2: National Tariffs & Package Masters
- **Target**: PM-JAY (Ayushman Bharat) and CGHS rate cards.
- **Finding**: PM-JAY Health Benefit Packages (HBP 2022) provides exact procedure-level pricing across 1,949 standard medical/surgical interventions. CGHS rate cards provide canonical room rent benchmarks (General ₹1,500, Semi-Private ₹3,000, Private ₹4,500, ICU ₹5,400 per day).
- **Decision**: Ingest PM-JAY and CGHS as the core baseline pricing tables.

## Discovery Session 3: Digital Health & Claims Architecture
- **Target**: ABDM Sandbox (HFR) and National Health Claims Exchange (NHCX).
- **Finding**: ABDM sandbox requires OAuth2 client credentials. NRCeS publishes comprehensive FHIR R4 profiles (`Coverage`, `Organization`, `Location`, `Claim`).
- **Decision**: Align database schemas and API payload serialization directly with NRCeS FHIR R4 profiles.
