from pydantic import BaseModel
from typing import List, Optional

class MatchRequest(BaseModel):
    patient_id: int
    lat: float
    lon: float
    procedure_code: str
    
class ExplainableOption(BaseModel):
    reason: str
    weight: float

class FacilityScore(BaseModel):
    hospital_id: int
    score: float
    reasons: List[ExplainableOption]
    
class RoomEligibilityResult(BaseModel):
    room_type: str
    eligible: bool
    
class ProportionateDeductionResult(BaseModel):
    net_patient_share: float
    deductions: float
    
class MatchResult(BaseModel):
    scores: List[FacilityScore]
