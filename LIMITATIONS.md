# System Limitations & Constraints — HOSPITALITY

## 1. Boundary of Capability

1. **Non-Medical Decision Support**:
   - The platform never offers clinical triage, diagnoses diseases, or recommends clinical care pathways.
   - It is strictly an informational and financial navigation aid.

2. **Indicative Financial Responsibility**:
   - Actual hospital bills depend on unforeseen clinical complications, dynamic surgical consumable consumption, individualized doctor fees, and final TPA claim adjudication.
   - All financial breakdowns are explicitly labelled as **INDICATIVE ESTIMATES**.

3. **No National Real-Time Bed API**:
   - No public, unified live bed availability feed currently operates across all private and public hospitals in India (post-COVID dashboards were decommissioned).
   - Bed counts in the prototype are powered by a realistic synthetic simulation engine tagged as `[SIMULATED]`.

4. **Proprietary Private Insurer Networks**:
   - Private insurers (e.g. Star Health, HDFC ERGO) do not expose real-time REST APIs for hospital network status.
   - Empanelment mappings are generated synthetically based on publicly known regional tie-up patterns and tagged as `[SIMULATED]`.
