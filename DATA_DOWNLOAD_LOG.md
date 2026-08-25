# Data Download & Acquisition Log — HOSPITALITY

**Log Date**: 2026-08-25  
**Protocol**: 3-Attempt Acquisition Hierarchy (Official API ➔ Official Download ➔ Synthetic Simulation)

---

## 📥 Dataset Acquisition Ledger

| Dataset ID | Source Organization | Acquisition Method | Status | File Saved | Records | Verification Notes |
|---|---|---|---|---|---|---|
| `DS-001` | Ministry of Health & Family Welfare (data.gov.in) | `DOWNLOAD_AVAILABLE` | **SUCCESS** | `data/processed/canonical_hospitals.json` | 8 Facilities | Verified coordinates, PIN codes, facility types across Bengaluru, Mumbai, Delhi. |
| `DS-002` | National Health Authority (PM-JAY HBP 2022) | `DOWNLOAD_AVAILABLE` | **SUCCESS** | `data/processed/pmjay_procedure_tariffs.json` | 8 Procedures | Verified NABH multipliers (+15%) and package codes (e.g. `CAR-002` Angioplasty). |
| `DS-003` | MoHFW Central Govt Health Scheme (CGHS) | `DOWNLOAD_AVAILABLE` | **SUCCESS** | `data/processed/cghs_room_tariffs.json` | 5 Categories | Verified room rent baselines: General (₹1.5k), Semi-Private (₹3k), Private (₹4.5k), ICU (₹5.4k). |
| `DS-004` | Private Insurers & State Health Schemes | `SIMULATED_FALLBACK` (Attempt 3) | **SUCCESS** | `data/processed/payers_schemes.json` | 8 Payers | Private insurer APIs are closed/proprietary. Generated realistic network empanelment mapping tagged `[SIMULATED]`. |
| `DS-005` | Real-time Bed Telemetry Feeds | `SIMULATED_FALLBACK` (Attempt 3) | **SUCCESS** | `data/processed/canonical_hospitals.json` | 40 Inventories | No public unified live bed API exists post-COVID. Generated synthetic telemetry tagged `[SIMULATED]`. |
