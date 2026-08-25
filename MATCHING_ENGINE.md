# Deterministic Matching & Proportionate Deduction Engine — HOSPITALITY

## 1. The Proportionate Deduction Trap in India

Under standard IRDAI retail health insurance clauses, if a policyholder occupies a room category with a tariff exceeding their allowed room rent cap:
1. The insurer pays only the allowed room rent rate.
2. **Crucially**, the insurer applies a proportionate reduction to **all associated medical expenses** (surgeon fees, OT charges, anesthesiologist fees, nursing charges, diagnostic tests).

### The Mathematical Formula

Let:
- $R_{\text{allowed}}$ = Policy daily room rent limit (e.g. ₹5,000/day).
- $R_{\text{actual}}$ = Actual hospital room tariff (e.g. ₹8,000/day for Deluxe Single).
- $N$ = Length of Stay in days (e.g. 4 days).
- $C_{\text{associated}}$ = Associated medical charges (e.g. ₹1,50,000 for Angioplasty OT + Surgeon + Diagnostics).
- $C_{\text{fixed}}$ = Non-proportionate fixed items (e.g. Cost of Stent/Implant = ₹35,000).
- $C_{\text{nonpayable}}$ = Excluded consumables/gloves/admin fees = ₹12,000.
- $P_{\text{copay}}$ = Policy copay percentage = 10%.

$$\text{Proportionate Factor } (\gamma) = \min\left(1.0, \frac{R_{\text{allowed}}}{R_{\text{actual}}}\right) = \frac{5,000}{8,000} = 0.625$$

$$\text{Payable Room Rent} = N \times R_{\text{allowed}} = 4 \times 5,000 = ₹20,000 \quad (\text{Patient excess: } 4 \times 3,000 = ₹12,000)$$

$$\text{Payable Associated} = C_{\text{associated}} \times \gamma = 1,50,000 \times 0.625 = ₹93,750 \quad (\text{Patient penalty: } ₹56,250)$$

$$\text{Total Admissible Claim} = \text{Payable Room Rent} + \text{Payable Associated} + C_{\text{fixed}} = 20,000 + 93,750 + 35,000 = ₹1,48,750$$

$$\text{Insurer Settlement (after Copay)} = \text{Total Admissible} \times (1 - P_{\text{copay}}) = 1,48,750 \times 0.90 = ₹1,33,875$$

$$\text{Total Hospital Bill} = (4 \times 8,000) + 1,50,000 + 35,000 + 12,000 = ₹2,29,000$$

$$\mathbf{\text{Total Patient Out-of-Pocket Share}} = \text{Total Bill} - \text{Insurer Settlement} = ₹2,29,000 - ₹1,33,875 = \mathbf{₹95,125}$$

> [!WARNING]
> By choosing a room that was ₹3,000/day more expensive (total ₹12,000 extra room charge), the patient suffered an out-of-pocket penalty of **₹95,125** instead of just ₹12,000. HOSPITALITY provides interactive previews to prevent this exact tragedy.

---

## 2. Multi-Criteria Hospital Match Scoring

Each hospital is scored for a patient scenario using normalized weights:

$$\text{Score} = w_e \cdot S_{\text{empanelment}} + w_c \cdot S_{\text{cost}} + w_d \cdot S_{\text{distance}} + w_b \cdot S_{\text{bed}}$$

- $w_e = 0.35$ (Empanelment Tier: Cashless Network = 1.0, Cashless Everywhere = 0.7, Reimbursement = 0.4).
- $w_c = 0.30$ (Cost/Room Index: Full Room Fit = 1.0, Minor Overage = 0.6, Massive Overage = 0.2).
- $w_d = 0.20$ (Proximity: $\exp(-d / 15\text{km})$).
- $w_b = 0.15$ (Real-time Bed Availability: Beds > 5 = 1.0, 1-4 Beds = 0.5, 0 Beds = 0.0).
