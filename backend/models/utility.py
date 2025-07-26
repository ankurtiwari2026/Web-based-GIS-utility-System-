from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from config.database import Base

class UtilityConsumption(Base):
    __tablename__ = "utility_consumption"
    
    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.id"))
    utility_type = Column(String, nullable=False)
    consumption_value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    recorded_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    building = relationship("Building", back_populates="utility_consumption")
