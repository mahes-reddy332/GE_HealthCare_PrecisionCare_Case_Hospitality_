# End-to-End Demo Script & Storyboard — HOSPITALITY

## Persona: Ramesh Kumar (Bengaluru, Karnataka)
- **Situation**: Ramesh's 68-year-old father requires an urgent elective Coronary Angioplasty with 1 stent.
- **Insurance**: Star Health Family Optima Floater (Sum Insured: ₹5,00,000, Room Rent Limit: 1% = ₹5,000/day, Copay: 10%).

---

## 🎬 5-Act Demonstration Flow

### Act 1: Policy Ingestion & Instant AI Extraction
- Ramesh uploads his policy certificate PDF to HOSPITALITY.
- The AI Extraction engine scans the PDF, highlights the relevant clauses with exact page citations, and populates the structured parameters: Sum Insured ₹5,00,000, Room Cap ₹5,000/day, Copay 10%.

### Act 2: Empanelled Hospital Discovery
- Ramesh selects specialty `Cardiology` and location `Bengaluru (15km radius)`.
- The system renders nearby facilities:
  - Apollo Hospital, Bannerghatta (Cashless Preferred, Match Score 96%)
  - Manipal Hospital, Old Airport Road (Cashless Network, Match Score 91%)
  - Fortis Hospital, Cunningham Road (Reimbursement Only, Match Score 78%)

### Act 3: The Room Rent Penalty Simulation (The "Aha!" Moment)
- Ramesh inspects Apollo Hospital's room options:
  - **Single Private A/C Room** (Tariff: ₹4,800/day): *Within Policy Cap*. Patient share = ₹14,500 (standard copay + non-payables).
  - **Deluxe Suite** (Tariff: ₹8,000/day): *Exceeds Policy Cap*. The simulator alerts Ramesh that this triggers a 37.5% proportionate deduction on associated OT and surgeon fees, spiking his out-of-pocket share to **₹72,400**.
- Ramesh chooses the Single Private A/C room, saving ₹57,900 in unexpected deductions.

### Act 4: Real-Time Bed Availability Check
- The system confirms that Apollo Hospital currently has 3 Single Private rooms and 2 ICU beds available.

### Act 5: Care Journey Navigation
- Ramesh activates the Care Journey tracking state machine:
  - Stage 1: `PRE_ADMISSION` ➔ Pre-auth checklist generated.
  - Stage 2: `ADMISSION` ➔ TPA desk intimation log recorded.
  - Stage 3: `PROCEDURE` ➔ Stent implant cost tagged as non-proportionate item.
  - Stage 4: `DISCHARGE` ➔ Itemized bill audit matching estimate within 5% tolerance.
