# FHIR R4 & NHCX Interoperability — HOSPITALITY

## 1. HL7 FHIR R4 Profile Alignment

HOSPITALITY adheres to the official National Resource Centre for EHR Standards (NRCeS) FHIR R4 implementation guides for India:

### Primary Resource Mappings
- **`Location`**: Physical hospital facility, latitude/longitude, operational status, bed capacity.
- **`Organization`**: Healthcare provider institution, empanelled insurance companies, accreditation bodies (NABH).
- **`HealthcareService`**: Specialized clinical departments (Cardiology, Oncology, Orthopedics).
- **`Coverage`**: Patient insurance policy terms, sum insured, room rent limits, copay rules.
- **`CoverageEligibilityRequest` / `Response`**: Real-time pre-authorization validation and benefit inquiry.
- **`Claim` / `ClaimResponse`**: Itemized procedure costs, room tariffs, and calculated deductions.

---

## 2. National Health Claims Exchange (NHCX)

The NHCX protocol standardizes electronic claims exchange across insurers, TPAs, and hospitals. HOSPITALITY formats its eligibility inquiry payloads according to NHCX FHIR bundles:

```json
{
  "resourceType": "CoverageEligibilityResponse",
  "id": "eligibility-resp-001",
  "status": "active",
  "purpose": ["benefits", "validation"],
  "patient": {
    "reference": "Patient/ABHA-91-8273-1928-11"
  },
  "insurance": [
    {
      "coverage": {
        "reference": "Coverage/STAR-FHO-500K"
      },
      "inforce": true,
      "item": [
        {
          "category": { "coding": [{ "code": "room-rent", "display": "Room Rent Limit" }] },
          "benefit": [{ "type": "financial", "allowedMoney": { "value": 5000, "currency": "INR" } }]
        },
        {
          "category": { "coding": [{ "code": "copay", "display": "Mandatory Co-payment" }] },
          "benefit": [{ "type": "financial", "allowedUnsignedInt": 10 }]
        }
      ]
    }
  ]
}
```
