# ABDM Health Facility Registry (HFR) Integration — HOSPITALITY

## 1. National Digital Health Architecture

The Ayushman Bharat Digital Mission (ABDM) manages the **Health Facility Registry (HFR)**, assigning unique identifiers to all healthcare providers in India across modern medicine, AYUSH, public, and private sectors.

```
+-------------------------------------------------------------------------+
|                       ABDM HFR INTEGRATION                              |
+-------------------------------------------------------------------------+
|  HFR Unique Identifier: IN2910000421                                    |
|  Verification Status: VERIFIED                                          |
|  Facility Type: Sub-District Hospital / Multi-Specialty                 |
|  System of Medicine: Allopathy                                          |
|  Ownership: Private For-Profit                                          |
|  ABDM M1 Milestone: ABHA Creation & Verification Enabled               |
|  ABDM M2 Milestone: Health Information Provider (HIP) Active            |
|  ABDM M3 Milestone: Health Information User (HIU) Active                |
+-------------------------------------------------------------------------+
```

## 2. Sandbox Integration Architecture
- **Auth Endpoint**: `POST https://dev.abdm.gov.in/gateway/v0.5/sessions`
- **HFR Sandbox Endpoint**: `https://facilitysbx.abdm.gov.in/v1.0/facilities/{facility_id}`
- **Security Headers**:
  - `Authorization: Bearer <JWT>`
  - `X-CM-ID: sbx`
  - `TIMESTAMP: <ISO-8601>`
  - `REQUEST-ID: <UUID-v4>`

HOSPITALITY records HFR IDs on canonical hospital entities, preparing the platform for full production ABDM M1-M3 certification.
