# Data Quality & Provenance Report — HOSPITALITY

## 1. Provenance & Confidence Tiers

Every record in the HOSPITALITY ecosystem is tagged with clear data reliability indicators:

```
                  +-----------------------------------+
                  |  HOSPITALITY DATA CONFIDENCE TIER |
                  +-----------------+-----------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
+-----------------------+                       +-----------------------+
|  AUTHORITATIVE TIER   |                       |    SIMULATED TIER     |
|  - data.gov.in (MoHFW)|                       |  - Live ICU Bed Feeds |
|  - PM-JAY HBP 2022    |                       |  - Private Insurer    |
|  - CGHS Rate Cards    |                       |    Cashless Tie-ups   |
|  Confidence: HIGH     |                       |  Confidence: SIMULATED|
+-----------------------+                       +-----------------------+
```

## 2. Integrity Verification Matrix

| Entity | Primary Source | Validation Rule | Null Handling | Quality Score |
|---|---|---|---|---|
| **Hospital Directory** | `data.gov.in` | Valid 6-digit Pincode, valid lat (-90 to 90), long (-180 to 180) | Impute city center coordinates if lat/long missing | 98.2% |
| **Package Tariffs** | `PM-JAY HBP 2022` | Numeric package rate > 0, valid specialty code | Flag missing NABH multiplier as standard rate | 99.5% |
| **Room Rates** | `CGHS Rate Cards` | Standard tiered rates (General, Semi-Private, Private, ICU) | Default to CGHS Metro baseline if hospital unlisted | 97.0% |
| **Policy Extractions**| `User PDF / LLM` | Sum Insured > 0, Room Rent type mapped to canonical enum | Prompt user for manual review if confidence < 0.70 | 94.0% |
