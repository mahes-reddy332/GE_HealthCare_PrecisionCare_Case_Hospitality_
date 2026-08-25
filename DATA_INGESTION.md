# Data Ingestion Engine & Pipelines — HOSPITALITY

## 1. Data Ingestion Architecture

```
Raw Sources (CSV / Excel / PDF / JSON / API)
                │
                ▼
      [ Data Provider Adapter ]
  ┌─────────────────────────────────┐
  │ - File reading & HTTP fetching  │
  │ - Encoding & null sanitation    │
  └─────────────────────────────────┘
                │
                ▼
       [ Normalization Layer ]
  ┌─────────────────────────────────┐
  │ - Canonical Entity Mapping      │
  │ - Address & Pincode standardization
  │ - Specialty Code taxonomy alignment
  └─────────────────────────────────┘
                │
                ▼
      [ Entity Resolution & Deduplication ]
  ┌─────────────────────────────────┐
  │ - Fuzzy name matching (>85%)    │
  │ - Geo-distance validation (<200m)│
  │ - Multi-source merge & scoring  │
  └─────────────────────────────────┘
                │
                ▼
      [ Unified Relational Database ]
```

## 2. Ingestion Pipelines

### Pipeline A: Hospital Directory Ingestion
- **Input**: `data.gov.in` hospital directory CSV/JSON.
- **Normalization**: Map state names to ISO/Standard nomenclature (e.g. `KA` ➔ `Karnataka`), clean pincodes (6-digit validation), extract phone numbers and email.
- **Enrichment**: Add ABDM HFR identifier stubs and assign synthetic private insurance network affiliations.

### Pipeline B: Package & Tariff Ingestion
- **Input**: `PM-JAY HBP 2022` master Excel + `CGHS` Standard Rate Cards.
- **Normalization**: Standardize procedure names (e.g. `Coronary Angioplasty` with ICD-10/specialty tagging `CAR`), extract base package rate, extract NABH rate multipliers (+15%).

### Pipeline C: Synthetic Bed Availability Engine
- **Algorithm**: Generates realistic bed capacities based on hospital category:
  - Tertiary/Teaching Medical Colleges: 500–1200 beds (15% ICU).
  - Multi-Specialty Private Hospitals: 100–350 beds (12% ICU).
  - Nursing Homes / Community Hospitals: 20–60 beds (5% ICU).
- Assigns real-time synthetic occupancy (e.g. 70–90% baseline occupancy) with periodic simulated drift.
