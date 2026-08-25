from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class OperationalStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    pincode = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    operational_status = Column(Enum(OperationalStatus), default=OperationalStatus.ACTIVE)
    
    identifiers = relationship("FacilityIdentifier", back_populates="hospital")
    specialties = relationship("FacilitySpecialty", back_populates="hospital")
    services = relationship("FacilityService", back_populates="hospital")
    rooms = relationship("BedInventory", back_populates="hospital")
    tariffs = relationship("Tariff", back_populates="hospital")
    schemes = relationship("HospitalScheme", back_populates="hospital")

class FacilityIdentifier(Base):
    __tablename__ = "facility_identifiers"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    system = Column(String) # HFR, ROHINI, NIN
    value = Column(String)
    
    hospital = relationship("Hospital", back_populates="identifiers")

class FacilitySpecialty(Base):
    __tablename__ = "facility_specialties"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String)
    
    hospital = relationship("Hospital", back_populates="specialties")

class FacilityService(Base):
    __tablename__ = "facility_services"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String)
    
    hospital = relationship("Hospital", back_populates="services")
