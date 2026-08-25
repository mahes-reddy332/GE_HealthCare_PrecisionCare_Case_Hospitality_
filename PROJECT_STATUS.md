# Project Status — HOSPITALITY

**Current State**: Phase -1 (Clean Reset) Completed ➔ Initializing Phase 0 (Data-Source Research & Foundation)  
**Last Updated**: 2026-08-25T13:43:30+05:30  
**Target Milestone**: GE Healthcare Precision Care Challenge 2026 Submission

---

## 🚦 Phase Tracking

| Phase | Title | Status | Description |
|---|---|---|---|
| **Phase -1** | **Complete Project Reset** | ✅ **COMPLETE** | Old implementation discarded; clean directory and doc suite established |
| **Phase 0** | **Data-Source Research & Ingestion Design** | 🔄 **IN PROGRESS** | Catalogue 30+ sources, define provenance, identify real vs synthetic data |
| **Phase 1** | **Canonical Data Model & Standards** | ⏳ **PENDING** | FHIR R4 mapping, relational ER schema, SQLite/Postgres DB setup |
| **Phase 2** | **Data Ingestion Engine** | ⏳ **PENDING** | Real data fetchers (data.gov.in, PM-JAY, CGHS) + synthetic generators |
| **Phase 3** | **Policy Intelligence & Extraction** | ⏳ **PENDING** | PDF parser, OCR, LLM extraction with confidence scores & clause citation |
| **Phase 4** | **Rule Engine & Proportionate Deduction** | ⏳ **PENDING** | Mathematical formulation of room rent caps, copays, non-payables |
| **Phase 5** | **Hospital & Room Matching Engine** | ⏳ **PENDING** | Multi-attribute scoring, distance filtering, empanelment verification |
| **Phase 6** | **FastAPI Backend Services** | ⏳ **PENDING** | Type-safe REST endpoints, Pydantic v2 schemas, provenance tags |
| **Phase 7** | **Care Journey State Machine** | ⏳ **PENDING** | 6-stage lifecycle tracking with stage-specific checklists & financial alerts |
| **Phase 8** | **Next.js Patient & Caregiver Dashboard** | ⏳ **PENDING** | Glanceable UI, Leaflet mapping, cost breakdown tables, confidence badges |
| **Phase 9** | **FHIR & NHCX Interoperability** | ⏳ **PENDING** | Export/import FHIR CoverageEligibility and Organization bundles |
| **Phase 10** | **End-to-End Demo & Validation** | ⏳ **PENDING** | 5-Act user journey validation, automated test suite, pitch deck sync |

---

## 🎯 Immediate Next Deliverables
1. Complete all 22 required initial root documentation blueprints.
2. Ingest primary public datasets into `data/raw/` (data.gov.in hospital samples, PM-JAY HBP packages, CGHS room rates).
3. Scaffold clean backend (`FastAPI`) and frontend (`Next.js`) with zero legacy contamination.
