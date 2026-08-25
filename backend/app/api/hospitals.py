from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..services.hospital_service import HospitalService
from ..schemas.hospital import HospitalResponse

router = APIRouter(prefix="/api/v1/hospitals", tags=["Hospitals"])

@router.get("", response_model=list[HospitalResponse])
async def list_hospitals(db: AsyncSession = Depends(get_db)):
    return await HospitalService.get_all_hospitals(db)

@router.get("/{id}")
async def get_hospital(id: int, db: AsyncSession = Depends(get_db)):
    return await HospitalService.get_hospital(db, id)
