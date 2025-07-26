from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from config.database import Base

class Complaint(Base):
    __tablename__ = "complaints"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    building_id = Column(Integer, ForeignKey("buildings.id"))
    category = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(Geometry('POINT', srid=4326))
    urgency_level = Column(String, nullable=False)
    status = Column(String, nullable=False, default="open")
    assigned_worker_id = Column(Integer, ForeignKey("users.id"))
    image_url = Column(String)
    priority_score = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="complaints", foreign_keys=[user_id])
    building = relationship("Building", back_populates="complaints")
    assigned_worker = relationship("User", back_populates="assigned_complaints", foreign_keys=[assigned_worker_id])
    updates = relationship("ComplaintUpdate", back_populates="complaint")

class ComplaintUpdate(Base):
    __tablename__ = "complaint_updates"
    
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    update_text = Column(Text, nullable=False)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    complaint = relationship("Complaint", back_populates="updates")
    user = relationship("User")
