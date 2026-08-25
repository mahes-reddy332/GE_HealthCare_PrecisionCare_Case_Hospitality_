# LLM & AI Architecture — HOSPITALITY

## 1. AI Safety & Mathematical Isolation Principle

> [!CAUTION]
> **STRICT LLM BOUNDARY**:  
> Large Language Models are probabilistic and prone to arithmetic hallucinations. In HOSPITALITY, the LLM is strictly confined to **unstructured text parsing, semantic entity extraction, and natural-language explanation generation**. The LLM is **NEVER** permitted to perform mathematical calculations for out-of-pocket costs, proportionate deductions, or room rent penalties. All arithmetic is executed by the deterministic Python Rule Engine.

```
+-----------------------------------------------------------------------------------+
|                            AI PIPELINE BOUNDARIES                                 |
+-----------------------------------------------------------------------------------+
|  [UNSTRUCTURED INPUT]                                                             |
|  - Policy PDF / Scanned Schedule / Raw Text                                       |
|                           │                                                       |
|                           ▼                                                       |
|  [LLM / NLP EXTRACTION LAYER]                                                     |
|  - Entity recognition (Insurer, Sum Insured, Room Rent Cap, Copay, Sublimits)    |
|  - Clause citation (Page number, exact quoted source text)                        |
|  - Extraction confidence score (0.00 - 1.00)                                       |
|                           │                                                       |
|                           ▼                                                       |
|  [STRUCTURED VALIDATION LAYER (Pydantic v2)]                                      |
|  - Strict type checking & boundary enforcement                                    |
|                           │                                                       |
|                           ▼                                                       |
|  [DETERMINISTIC RULE ENGINE (Pure Python)]                                        |
|  - Proportionate deduction algebra                                                |
|  - Copay and deductible arithmetic                                                |
|  - Multi-hospital ranking scores                                                  |
|                           │                                                       |
|                           ▼                                                       |
|  [LLM EXPLANATION GENERATOR]                                                      |
|  - Plain-language translation of mathematical outputs for stressed caregivers    |
+-----------------------------------------------------------------------------------+
```

## 2. Extraction Schema

The LLM extraction produces a typed JSON structure matching:
```json
{
  "insurer_name": "Star Health and Allied Insurance",
  "plan_name": "Family Health Optima Insurance Plan",
  "sum_insured": 500000,
  "room_rent_limit_type": "PERCENTAGE_OF_SI",
  "room_rent_limit_value": 1.0,
  "room_rent_max_daily_inr": 5000,
  "icu_limit_type": "PERCENTAGE_OF_SI",
  "icu_limit_value": 2.0,
  "copay_percentage": 10.0,
  "deductible_amount": 0,
  "exclusions": [
    {
      "category": "MATERNITY",
      "description": "Maternity expenses not covered in first 24 months",
      "page_number": 3,
      "source_text": "Section 4.1: Maternity expenses are excluded..."
    }
  ],
  "overall_confidence": 0.94
}
```
