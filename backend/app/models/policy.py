from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Policy(Base):
    __tablename__ = "policies"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    policy_number = Column(String)
    insurer = Column(String)
    sum_insured = Column(Float)
    room_rent_cap_type = Column(String)
    room_rent_limit = Column(Float)
    icu_limit = Column(Float)
    copay_percentage = Column(Float, default=0)
    deductible = Column(Float, default=0)
    
    exclusions = relationship("PolicyExclusion", back_populates="policy")
    extractions = relationship("PolicyExtractionClause", back_populates="policy")

class PolicyExclusion(Base):
    __tablename__ = "policy_exclusions"
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"))
    description = Column(String)
    
    policy = relationship("Policy", back_populates="exclusions")

class PolicyExtractionClause(Base):
    __tablename__ = "policy_extraction_clauses"
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"))
    clause_type = Column(String)
    source_text = Column(String)
    page_number = Column(Integer)
    confidence = Column(String)
    
    policy = relationship("Policy", back_populates="extractions")
