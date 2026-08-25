from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class FacilityIdentifierSchema(BaseModel):
    id: Optional[int] = None
    system: str
    value: str

    class Config:
        from_attributes = True

class FacilitySpecialtySchema(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True

class BedInventorySchema(BaseModel):
    id: Optional[int] = None
    room_type: str
    total: int
    occupied: int
    available: int
    last_updated: Optional[datetime] = None
    data_status: str = "SIMULATED"

    class Config:
        from_attributes = True

class TariffSchema(BaseModel):
    id: Optional[int] = None
    specialty_code: str
    procedure_code: str
    procedure_name: str
    package_rate: float
    nabh_rate: Optional[float] = None
    preauth_required: bool = False
    source: str = "PMJAY_HBP_2022"

    class Config:
        from_attributes = True

class HospitalResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    city: str
    state: str
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    operational_status: str = "ACTIVE"
    identifiers: List[FacilityIdentifierSchema] = []
    specialties: List[FacilitySpecialtySchema] = []
    rooms: List[BedInventorySchema] = []
    tariffs: List[TariffSchema] = []

    class Config:
        from_attributes = True

class HospitalSearchParams(BaseModel):
    city: Optional[str] = None
    specialty: Optional[str] = None
    payer: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    radius_km: Optional[float] = 15.0

class HospitalComparisonResponse(BaseModel):
    hospitals: List[HospitalResponse]
    comparison_matrix: Dict[str, Any] = {}
