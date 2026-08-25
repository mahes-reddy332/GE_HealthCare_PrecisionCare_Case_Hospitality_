from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum

class RoomType(str, enum.Enum):
    GENERAL = "General"
    SEMI_PRIVATE = "Semi-Private"
    PRIVATE_AC = "Private AC"
    DELUXE = "Deluxe"
    ICU = "ICU"

class BedInventory(Base):
    __tablename__ = "bed_inventories"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    room_type = Column(Enum(RoomType))
    total = Column(Integer)
    occupied = Column(Integer)
    available = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)
    data_status = Column(String, default="SIMULATED")
    
    hospital = relationship("Hospital", back_populates="rooms")
