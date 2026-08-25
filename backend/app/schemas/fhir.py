from pydantic import BaseModel
from typing import List, Optional

class FHIRLocation(BaseModel):
    resourceType: str = "Location"
    id: str
    name: str

class FHIROrganization(BaseModel):
    resourceType: str = "Organization"
    id: str
    name: str

class FHIRCoverage(BaseModel):
    resourceType: str = "Coverage"
    id: str
    status: str

class FHIRCovEligibilityRequest(BaseModel):
    resourceType: str = "CoverageEligibilityRequest"
    patient_id: str

class FHIRCovEligibilityResponse(BaseModel):
    resourceType: str = "CoverageEligibilityResponse"
    status: str
    
class FHIRClaim(BaseModel):
    resourceType: str = "Claim"
    status: str
