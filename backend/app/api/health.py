from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/health")
@router.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "HOSPITALITY API",
        "version": "2.0.0",
        "standards": ["HL7 FHIR R4", "ABDM HFR", "NHCX"],
        "database": "connected"
    }
