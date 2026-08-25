# HOSPITALITY
### Holistic Optimization System for Policy-Integrated Admission & Treatment Intelligence

[![GE Healthcare Precision Care Challenge 2026](https://img.shields.io/badge/GE%20Healthcare-Precision%20Care%20Challenge%202026-005EB8.svg)](https://www.gehealthcare.in/)
[![Status](https://img.shields.io/badge/Status-Clean%20Rebuild%20Phase%200-success.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FHIR R4](https://img.shields.io/badge/Standard-HL7%20FHIR%20R4%20%2F%20ABDM-orange.svg)](https://nrces.in/ndhm/fhir/r4/)

---

> [!IMPORTANT]
> **LEGAL & MEDICAL DECISION-SUPPORT DISCLAIMER**  
> HOSPITALITY is an explainable decision-support and navigation tool for healthcare consumers, caregivers, and medical coordinators. It is **NOT** a medical diagnostic device, does **NOT** provide clinical triage, and does **NOT** issue legally binding insurance claim pre-authorizations or guarantee final reimbursement amounts. All financial projections, room category eligibilities, and out-of-pocket shares are indicative, calculated from publicly verifiable rate baselines, user-provided policy terms, and synthetic simulation models.

---

## 🏥 Problem Overview

During emergency and planned hospital admissions across India, patients and caregivers face acute financial opacity and fragmented information:
1. **Uncertain Hospital Empanelment**: Unclear whether a facility accepts the patient's specific private insurer (e.g. Star Health, HDFC ERGO) or public scheme (PM-JAY, CGHS, State schemes like Arogya Karnataka).
2. **Room Rent Traps & Proportionate Deductions**: Exceeding the policy's room rent limit triggers draconian proportionate deductions on associated surgeon fees, diagnostics, and OT charges under IRDAI guidelines.
3. **Bed Availability & Capacity Opacity**: No single unified national public API exists for real-time live bed occupancy.
4. **Complex Non-Payables**: Consumables, admin charges, and unapproved package exclusions lead to unexpected out-of-pocket hospital bills.

---

## 🎯 Solution Architecture & Core Flow

HOSPITALITY harmonizes policy terms, hospital directories, empanelment networks, room inventories, and procedure tariffs into an explainable, unified decision pipeline:

```
PATIENT POLICY (PDF/Manual)
      ↓
POLICY EXTRACTION (LLM / Structured Parser)
      ↓
NORMALIZED POLICY (FHIR Coverage Standard)
      ↓
POLICY CONSTRAINTS (Room Caps, Co-pay, Deductibles, Sub-limits)
      ↓
INSURANCE NETWORK (Empanelment & Cashless Mapping)
      ↓
HOSPITAL / FACILITY (Location, Infrastructure, Accreditation)
      ↓
ROOM / BED (General, Semi-Private, Private, ICU Capacity)
      ↓
COST + COVERAGE ESTIMATE (CGHS/PM-JAY Tariffs vs Policy Limits)
      ↓
NHCX / FHIR INTEROPERABILITY (Standardized Payloads)
      ↓
MATCHING ENGINE (Deterministic Scoring & Constraint Evaluation)
      ↓
EXPLAINABLE OPTIONS (Proportionate Deduction Warnings & Math Proofs)
      ↓
PATIENT DASHBOARD (Glanceable UI & Care Journey State Machine)
```

---

## 🛠️ Technology Stack

* **Backend**: Python 3.11+, FastAPI, SQLAlchemy 2.0 (Async), Pydantic v2, SQLite / PostgreSQL.
* **Frontend**: Next.js 14/15 App Router, TypeScript, Tailwind CSS, Lucide Icons, Recharts.
* **Standards & AI**: HL7 FHIR R4, ABDM Health Facility Registry specifications, NHCX claims exchange schemas, Gemini/Mock LLM policy intelligence.
* **Data Sources**: data.gov.in (Hospital Directory with Geo Codes), PM-JAY HBP 2022 Package Master, CGHS Standard Rate Cards, OpenStreetMap Overpass API, ABDM Sandbox.

---

## 📂 Repository Structure

```
HOSPITALITY/
├── README.md                 # Primary system guide and overview
├── PROJECT_STATUS.md         # Real-time phase tracking and milestones
├── IMPLEMENTATION_PLAN.md    # Multi-phase master implementation blueprint
├── CHANGELOG.md              # Version history and changes
├── ARCHITECTURE.md           # Deep architectural specification
├── DATA_SOURCE_REGISTRY.md   # Complete catalogue of 30+ Indian health datasets
├── DATA_INGESTION.md         # Ingestion pipelines and normalization rules
├── DATA_DICTIONARY.md        # Canonical entity schemas and data models
├── LLM_ARCHITECTURE.md       # Policy extraction and NLP design
├── INSURANCE_NETWORK.md      # Empanelment and cashless network model
├── ABDM_HFR.md               # Health Facility Registry integration spec
├── FHIR_NHCX.md              # FHIR R4 and Claims Exchange profile mapping
├── MATCHING_ENGINE.md        # Mathematical formulation of coverage and deductions
├── API_SPECIFICATION.md      # REST API contracts
├── DASHBOARD_SPECIFICATION.md# UI/UX design system and view layout
├── DATA_QUALITY_REPORT.md    # Provenance tracking, quality checks, and confidence tiers
├── LIMITATIONS.md            # Transparent operational constraints
├── RESEARCH_LOG.md           # Verified discovery logs of Indian public data
├── DECISIONS.md              # Architecture Decision Records (ADRs)
├── DEMO_SCRIPT.md            # Step-by-step 5-act judging demonstration
├── PPT_CONTENT.md            # Phase 1 submission presentation alignment
├── CLEAN_START.md            # Clean reset declaration
│
├── frontend/                 # Next.js client application
├── backend/                  # FastAPI service, database models, API routers
├── data/                     # Raw, processed, external, and synthetic data
├── references/               # Challenge specifications, policies, research papers
├── scripts/                  # Data fetchers, seeders, and validation scripts
├── tests/                    # Unit, integration, and rule engine tests
└── docker/                   # Container definitions
```

---

## 🚀 Getting Started

### Prerequisites
* Python 3.11+
* Node.js 18+ / npm

### Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 📜 License
MIT License. Built for the GE Healthcare Precision Care Challenge 2026.
