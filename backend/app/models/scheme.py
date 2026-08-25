from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Scheme(Base):
    __tablename__ = "schemes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # e.g. PM-JAY, CGHS, Star Health
    type = Column(String) # GOVERNMENT, PRIVATE
    
    hospital_mappings = relationship("HospitalScheme", back_populates="scheme")

class HospitalScheme(Base):
    __tablename__ = "hospital_schemes"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    scheme_id = Column(Integer, ForeignKey("schemes.id"))
    cashless_available = Column(Boolean, default=False)
    
    hospital = relationship("Hospital", back_populates="schemes")
    scheme = relationship("Scheme", back_populates="hospital_mappings")

class InsuranceNetwork(Base):
    __tablename__ = "insurance_networks"
    id = Column(Integer, primary_key=True, index=True)
    insurer = Column(String)
    product = Column(String)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    cashless_status = Column(Boolean, default=False)
    tpa = Column(String)
