from fastapi import APIRouter
router = APIRouter(prefix="/api/v1/patients", tags=["Journey"])

@router.get("/{id}/journey")
async def get_journey(id: int):
    return {"message": "mock journey"}
