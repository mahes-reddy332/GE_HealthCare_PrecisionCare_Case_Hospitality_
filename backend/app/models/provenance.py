from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from ..database import Base
import enum
from datetime import datetime

class DataStatus(str, enum.Enum):
    AUTHORITATIVE = "AUTHORITATIVE"
    PUBLIC_VERIFIED = "PUBLIC_VERIFIED"
    SIMULATED = "SIMULATED"

class ConfidenceLevel(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(Enum(DataStatus))
    url = Column(String)

class DataRecord(Base):
    __tablename__ = "data_records"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("data_sources.id"))
    retrieved_at = Column(DateTime, default=datetime.utcnow)
    data_status = Column(Enum(DataStatus))
    confidence = Column(Enum(ConfidenceLevel))
    
    source = relationship("DataSource")
