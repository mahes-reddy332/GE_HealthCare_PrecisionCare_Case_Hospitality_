# Data Dictionary & Canonical Schema — HOSPITALITY

## 1. Relational Entities

### `hospitals`
| Field | Type | Description |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY` | Internal unique identifier |
| `name` | `VARCHAR` | Official facility name |
| `facility_type` | `VARCHAR` | `GOVERNMENT_TERTIARY`, `PRIVATE_MULTISPECIALTY`, `COMMUNITY_HEALTH_CENTRE` |
| `ownership` | `VARCHAR` | `PUBLIC`, `PRIVATE_FOR_PROFIT`, `PRIVATE_TRUST` |
| `address` | `VARCHAR` | Complete street address |
| `city` | `VARCHAR` | City/Town name |
| `district` | `VARCHAR` | Administrative district |
| `state` | `VARCHAR` | Standard state name |
| `pincode` | `VARCHAR(6)` | 6-digit postal code |
| `latitude` | `FLOAT` | Geographic latitude |
| `longitude` | `FLOAT` | Geographic longitude |
| `phone` | `VARCHAR` | Primary contact number |
| `email` | `VARCHAR` | Official hospital contact email |
| `total_beds` | `INTEGER` | Total bed capacity |
| `icu_beds` | `INTEGER` | Total intensive care unit beds |
| `emergency_available` | `BOOLEAN` | 24x7 Emergency services available |
| `nabh_accredited` | `BOOLEAN` | National Accreditation Board for Hospitals certified |
| `operational_status` | `VARCHAR` | `OPERATIONAL`, `DECOMMISSIONED` |

### `room_types`
| Field | Type | Description |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY` | Room type ID |
| `hospital_id` | `INTEGER FK` | Reference to `hospitals.id` |
| `category` | `VARCHAR` | `GENERAL_WARD`, `SEMI_PRIVATE`, `PRIVATE_AC`, `DELUXE`, `ICU`, `HDU`, `NICU` |
| `name` | `VARCHAR` | Hospital-specific room naming |
| `daily_tariff` | `FLOAT` | Daily room rent in INR |
| `data_status` | `VARCHAR` | `AUTHORITATIVE`, `PUBLIC_VERIFIED`, `SIMULATED` |

### `bed_inventories`
| Field | Type | Description |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY` | Inventory ID |
| `hospital_id` | `INTEGER FK` | Reference to `hospitals.id` |
| `room_type_id` | `INTEGER FK` | Reference to `room_types.id` |
| `total_beds` | `INTEGER` | Total beds in this category |
| `available_beds` | `INTEGER` | Currently unoccupied/available beds |
| `occupied_beds` | `INTEGER` | Currently occupied beds |
| `last_updated` | `DATETIME` | Timestamp of inventory update |
| `data_status` | `VARCHAR` | `SIMULATED` |

### `tariffs`
| Field | Type | Description |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY` | Tariff ID |
| `hospital_id` | `INTEGER FK` | Reference to `hospitals.id` (nullable for generic packages) |
| `scheme_id` | `INTEGER FK` | Reference to public/private scheme (nullable) |
| `specialty_code` | `VARCHAR` | Code (e.g. `CAR`, `ONC`, `ORT`) |
| `procedure_name` | `VARCHAR` | Standard procedure name |
| `package_rate` | `FLOAT` | Base total package cost in INR |
| `nabh_rate` | `FLOAT` | Rate with NABH accreditation markup |
| `preauth_required` | `BOOLEAN` | Whether pre-authorization is mandatory |
| `source` | `VARCHAR` | `PMJAY_HBP`, `CGHS`, `HOSPITAL_SCHEDULE`, `SIMULATED` |

### `policies`
| Field | Type | Description |
|---|---|---|
| `id` | `INTEGER PRIMARY KEY` | Policy ID |
| `policy_number` | `VARCHAR` | User policy certificate number |
| `insurer_name` | `VARCHAR` | Insurance company name (e.g. Star Health) |
| `policy_type` | `VARCHAR` | `INDIVIDUAL_RETAIL`, `FAMILY_FLOATER`, `GROUP_CORPORATE` |
| `sum_insured` | `FLOAT` | Total annual coverage amount in INR |
| `room_rent_type` | `VARCHAR` | `PERCENTAGE_OF_SI`, `FIXED_DAILY_CAP`, `SPECIFIC_CATEGORY`, `NO_CAPPING` |
| `room_rent_limit` | `FLOAT` | Allowed daily room rent in INR or percentage |
| `icu_limit` | `FLOAT` | Allowed daily ICU rent in INR |
| `copay_percentage` | `FLOAT` | Mandatory user co-pay (e.g. 10.0%) |
| `deductible` | `FLOAT` | Aggregate or per-claim deductible |
| `extraction_confidence`| `FLOAT` | Confidence score of AI extraction (0.0 - 1.0) |
