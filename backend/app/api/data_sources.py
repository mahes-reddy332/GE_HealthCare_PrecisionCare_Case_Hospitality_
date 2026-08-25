from fastapi import APIRouter
router = APIRouter(prefix="/api/v1", tags=["DataSources"])

@router.get("/data-sources")
async def data_sources():
    return []
