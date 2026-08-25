# Patient AI Chatbot Specification — HOSPITALITY

## 1. Safety & Determinism Architecture
The Patient AI Chatbot uses **Tool-Augmented Retrieval & Execution**. The conversational model does NOT invent facts, coverage terms, bed availability, or financial arithmetic from ungrounded weights.

```
USER QUESTION (e.g. "Is Deluxe room covered at Apollo?")
                 │
                 ▼
       [ Intent Recognizer ]
                 │
                 ▼
     [ Tool Execution Pipeline ]
 ┌──────────────────────────────────────────────┐
 │ 1. Query Active Policy (Room cap: ₹5,000)   │
 │ 2. Query Hospital Tariff (Deluxe: ₹9,000)   │
 │ 3. Execute Proportionate Deduction Math     │
 │ 4. Extract Clause Citations (Section 3.1)   │
 └──────────────────────────────────────────────┘
                 │
                 ▼
  [ LLM Explanation & Response Generator ]
  - Transparent mathematical breakdown
  - Source citations with page numbers
  - Actionable guidance & warnings
```
