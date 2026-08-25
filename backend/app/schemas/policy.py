from pydantic import BaseModel
from typing import List, Optional

class PolicyCreate(BaseModel):
    policy_number: str
    insurer: str
    sum_insured: float

class PolicyResponse(BaseModel):
    id: int
    policy_number: str
    insurer: str
    sum_insured: float

    class Config:
        from_attributes = True

class PolicyExtracted(BaseModel):
    sum_insured: float
    room_rent_cap_type: str
    room_rent_limit: float
    icu_limit: float
    copay_percentage: float
    deductible: float

class PolicyUploadResponse(BaseModel):
    message: str
    extracted_data: PolicyExtracted
