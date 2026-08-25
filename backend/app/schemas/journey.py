from pydantic import BaseModel
from typing import List
from datetime import datetime
from ..models.patient import JourneyEvent

class JourneyEventCreate(BaseModel):
    event_type: JourneyEvent
    description: str

class JourneyEventResponse(BaseModel):
    id: int
    event_type: JourneyEvent
    description: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class JourneyResponse(BaseModel):
    id: int
    current_stage: JourneyEvent
    events: List[JourneyEventResponse]
    
    class Config:
        from_attributes = True
