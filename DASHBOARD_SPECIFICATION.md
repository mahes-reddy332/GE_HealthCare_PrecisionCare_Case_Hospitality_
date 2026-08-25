# Patient Dashboard Specification & UI System — HOSPITALITY

## 1. Design Philosophy for Stressed Caregivers
When navigating medical admissions, patients and caregivers experience high cognitive fatigue and emotional distress. The HOSPITALITY interface prioritizes:
1. **Calm Color Palette**: Deep healthcare blues (`#005EB8`), soft neutrals (`#F8FAFC`), and crisp semantic accents (Emerald Green for covered, Amber for warnings, Slate for simulated).
2. **Glanceable Metrics**: High-contrast summary cards showing estimated out-of-pocket share, room eligibility, and network status without complex jargon.
3. **Transparent Mathematical Proofs**: Every cost number can be expanded into an itemized mathematical audit with formula breakdowns and policy clause citations.
4. **Unambiguous Data Badges**: Prominent badges identifying data reliability (`AUTHORITATIVE`, `PUBLIC_VERIFIED`, `SIMULATED`).

---

## 2. Core Views & User Journeys

```
+-----------------------------------------------------------------------------------+
| [HOSPITALITY NAV]  Dashboard | Hospitals | Policy Intelligence | Care Journey | Ops|
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [!] DISCLAIMER: Non-clinical decision support. All financial estimates indicative|
|                                                                                   |
|  +---------------------------+  +-----------------------------------------------+  |
|  | ACTIVE POLICY SUMMARY     |  | REAL-TIME CARE JOURNEY                        |  |
|  | Star Health Family Optima |  | [Pre-Admission] > [ADMISSION] > [Discharge]   |  |
|  | Sum Insured: ₹5,00,000    |  | Current Stage: Room Selection & Pre-Auth      |  |
|  | Room Rent Cap: ₹5,000/day |  | Checklist: Submit TPA pre-auth form within 3h|  |
|  +---------------------------+  +-----------------------------------------------+  |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | NEARBY EMPANELLED HOSPITALS (Bengaluru - 15km Radius)                       |  |
|  | Filter: [Specialty: Cardiology v] [Scheme: Star Health v] [Show Cashless Only]|  |
|  |                                                                             |  |
|  |  [Card 1] Apollo Hospital, Bannerghatta                                     |  |
|  |  Status: CASHLESS PREFERRED | Match Score: 96% | Beds Avail: 14 (ICU: 3)    |  |
|  |  Room Fit: General (₹1.8k) [Covered] | Single A/C (₹5.2k) [Minor Copay]     |  |
|  |  Estimated Out-of-Pocket: ₹14,200 (Breakdown Available)                     |  |
|  |                                                                             |  |
|  |  [Card 2] Manipal Hospital, Old Airport Road                                |  |
|  |  Status: CASHLESS NETWORK   | Match Score: 91% | Beds Avail: 8 (ICU: 1)     |  |
|  |  Room Fit: Deluxe A/C (₹8.5k) [!] WARNING: Triggers ₹42,000 Penalty        |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```
