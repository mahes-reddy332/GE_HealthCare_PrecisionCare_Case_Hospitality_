from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from ..database import get_db
from ..models.hospital import Hospital
from ..models.policy import Policy

router = APIRouter(prefix="/api/v1/fhir", tags=["HL7 FHIR R4 & NHCX Interoperability"])

@router.get("/Location/{id}")
async def get_fhir_location(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Hospital).where(Hospital.id == id).options(selectinload(Hospital.identifiers)))
    h = result.scalar_one_or_none()
    if not h:
        raise HTTPException(status_code=404, detail="Hospital location not found")
    
    hfr_id = next((i.value for i in h.identifiers if i.system == "HFR"), f"IN291000{h.id:04d}")

    return {
        "resourceType": "Location",
        "id": f"loc-{h.id}",
        "identifier": [
            {
                "system": "https://facility.abdm.gov.in",
                "value": hfr_id
            }
        ],
        "status": "active",
        "name": h.name,
        "mode": "instance",
        "type": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-RoleCode",
                        "code": "HOSP",
                        "display": "Hospital"
                    }
                ]
            }
        ],
        "address": {
            "use": "work",
            "line": [h.address],
            "city": h.city,
            "state": h.state,
            "postalCode": h.pincode,
            "country": "IND"
        },
        "position": {
            "latitude": h.latitude,
            "longitude": h.longitude
        }
    }

@router.get("/Coverage/{id}")
async def get_fhir_coverage(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Policy).where(Policy.id == id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Policy coverage not found")

    return {
        "resourceType": "Coverage",
        "id": f"cov-{p.id}",
        "identifier": [
            {
                "system": "https://irdai.gov.in/policies",
                "value": p.policy_number
            }
        ],
        "status": "active",
        "kind": "insurance",
        "beneficiary": {
            "reference": "Patient/ABHA-91-8273-1928-1144"
        },
        "payor": [
            {
                "display": p.insurer
            }
        ],
        "costToBeneficiary": [
            {
                "type": {
                    "coding": [{ "code": "copay", "display": "Mandatory Co-Payment" }]
                },
                "valueQuantity": {
                    "value": p.copay_percentage,
                    "unit": "%"
                }
            },
            {
                "type": {
                    "coding": [{ "code": "room-rent-cap", "display": "Daily Room Rent Cap" }]
                },
                "valueMoney": {
                    "value": p.room_rent_limit,
                    "currency": "INR"
                }
            }
        ]
    }

@router.post("/CoverageEligibilityRequest")
async def process_eligibility_request(payload: dict):
    return {
        "resourceType": "CoverageEligibilityResponse",
        "id": "nhcx-resp-88192",
        "status": "active",
        "purpose": ["benefits", "validation"],
        "patient": {
            "reference": "Patient/ABHA-91-8273-1928-1144"
        },
        "created": "2026-08-25T13:50:00Z",
        "insurer": {
            "display": "Star Health and Allied Insurance"
        },
        "outcome": "complete",
        "disposition": "Policy is in-force and cashless authorization is eligible at this facility.",
        "insurance": [
            {
                "inforce": True,
                "benefitBalance": [
                    {
                        "category": { "coding": [{ "code": "room-rent", "display": "Room Rent Limit" }] },
                        "financial": [
                            { "type": { "coding": [{ "code": "allowed" }] }, "allowedMoney": { "value": 5000, "currency": "INR" } }
                        ]
                    }
                ]
            }
        ]
    }
