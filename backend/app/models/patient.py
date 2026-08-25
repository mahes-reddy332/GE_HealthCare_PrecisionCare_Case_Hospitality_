from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum

class JourneyEvent(str, enum.Enum):
    PRE_ADMISSION = "PRE_ADMISSION"
    HOSPITAL_SELECTION = "HOSPITAL_SELECTION"
    PRE_AUTH = "PRE_AUTH"
    ADMISSION = "ADMISSION"
    INVESTIGATION = "INVESTIGATION"
    PROCEDURE = "PROCEDURE"
    RECOVERY = "RECOVERY"
    DISCHARGE = "DISCHARGE"
    CLAIM = "CLAIM"

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    abha_id = Column(String, nullable=True)
    phone = Column(String)
    
    journeys = relationship("PatientJourney", back_populates="patient")

class PatientJourney(Base):
    __tablename__ = "patient_journeys"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    current_stage = Column(Enum(JourneyEvent))
    start_date = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="journeys")
    events = relationship("JourneyEventLog", back_populates="journey")

class JourneyEventLog(Base):
    __tablename__ = "journey_events"
    id = Column(Integer, primary_key=True, index=True)
    journey_id = Column(Integer, ForeignKey("patient_journeys.id"))
    event_type = Column(Enum(JourneyEvent))
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    journey = relationship("PatientJourney", back_populates="events")
