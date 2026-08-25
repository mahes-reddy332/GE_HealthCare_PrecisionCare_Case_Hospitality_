from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Tariff(Base):
    __tablename__ = "tariffs"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    specialty_code = Column(String)
    procedure_code = Column(String)
    procedure_name = Column(String)
    package_rate = Column(Float)
    nabh_rate = Column(Float, nullable=True)
    preauth_required = Column(Boolean, default=False)
    source = Column(String) # PMJAY, CGHS, HOSPITAL
    
    hospital = relationship("Hospital", back_populates="tariffs")
