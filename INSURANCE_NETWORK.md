# Insurance Network & Empanelment Model — HOSPITALITY

## 1. Network Status Taxonomy

In India, hospital admission coverage depends heavily on the facility's formal relationship with the patient's insurer or Third-Party Administrator (TPA):

1. **`CASHLESS_NETWORK` (Tier 1 Preferred)**:
   - Direct empanelment with the insurer or TPA (e.g. GIPSA PPN, Medi Assist, Vidal Health).
   - Patient pays only non-payables and applicable copays at discharge; hospital bills insurer directly after pre-auth.
2. **`CASHLESS_EVERYWHERE` (Tier 2 Interoperable)**:
   - Under IRDAI's 2024 "Cashless Everywhere" framework, facilities with 15+ beds can offer cashless treatment even without prior empanelment, provided 48-hour advance intimation (or 3-hour emergency intimation) is given.
3. **`REIMBURSEMENT_ONLY` (Tier 3)**:
   - Patient pays full hospital bill upfront at discharge and files claim documents post-discharge with insurer.
4. **`EXCLUDED_BLACKLISTED` (Tier 4 Prohibited)**:
   - Facilities excluded by insurers due to historical fraud or compliance investigations. Zero claim admissibility.

## 2. Synthetic Empanelment Allocation Matrix

To simulate comprehensive multi-payer hospital search in the prototype, hospitals are mapped across key payers:
- **Private Insurers**: Star Health, HDFC ERGO, ICICI Lombard, Care Health, Niva Bupa, Bajaj Allianz.
- **Government Schemes**: PM-JAY (Ayushman Bharat), CGHS (Central Govt), ESI, SAST (Arogya Karnataka).
- **TPAs**: Medi Assist, Paramount TPA, Vidal Health, Heritage Health.
