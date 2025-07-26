from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from config.database import Base

class Building(Base):
    __tablename__ = "buildings"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    location = Column(Geometry('POINT', srid=4326))
    building_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    residents = relationship("User", back_populates="building")
    complaints = relationship("Complaint", back_populates="building")
    utility_consumption = relationship("UtilityConsumption", back_populates="building")
