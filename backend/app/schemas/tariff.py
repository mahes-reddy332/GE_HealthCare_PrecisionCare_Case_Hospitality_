from pydantic import BaseModel

class TariffResponse(BaseModel):
    id: int
    procedure_code: str
    procedure_name: str
    package_rate: float
    
    class Config:
        from_attributes = True

class CostBreakdownEstimate(BaseModel):
    procedure_cost: float
    room_cost: float
    total: float

class FinancialResponsibility(BaseModel):
    insurance_pays: float
    patient_pays: float
