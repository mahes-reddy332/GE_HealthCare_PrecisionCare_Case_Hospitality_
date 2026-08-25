from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..models.hospital import Hospital

class HospitalService:
    @staticmethod
    async def get_all_hospitals(db: AsyncSession, city: str = None, specialty: str = None):
        query = select(Hospital).options(
            selectinload(Hospital.identifiers),
            selectinload(Hospital.specialties),
            selectinload(Hospital.rooms),
            selectinload(Hospital.tariffs),
            selectinload(Hospital.schemes)
        )
        if city:
            query = query.where(Hospital.city.ilike(f"%{city}%"))
        result = await db.execute(query)
        return result.scalars().all()
    
    @staticmethod
    async def get_hospital(db: AsyncSession, hospital_id: int):
        query = select(Hospital).where(Hospital.id == hospital_id).options(
            selectinload(Hospital.identifiers),
            selectinload(Hospital.specialties),
            selectinload(Hospital.rooms),
            selectinload(Hospital.tariffs),
            selectinload(Hospital.schemes)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
