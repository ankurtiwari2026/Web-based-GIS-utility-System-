from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from config.database import get_db
from models.complaint import Complaint, ComplaintUpdate
from models.user import User
from ml.complaint_prioritizer import ComplaintPrioritizer
import json

router = APIRouter()

class ComplaintCreate(BaseModel):
    category: str
    title: str
    description: str
    latitude: float
    longitude: float
    urgency_level: str
    building_id: int

class ComplaintResponse(BaseModel):
    id: int
    category: str
    title: str
    description: str
    latitude: float
    longitude: float
    urgency_level: str
    status: str
    priority_score: float
    created_at: datetime
    user_name: str
    building_name: str
    assigned_worker_name: Optional[str] = None

class ComplaintUpdateCreate(BaseModel):
    update_text: str
    status: Optional[str] = None

@router.post("/create", response_model=dict)
async def create_complaint(
    complaint: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create complaint with PostGIS point
    location_point = func.ST_GeomFromText(f'POINT({complaint.longitude} {complaint.latitude})', 4326)
    
    db_complaint = Complaint(
        user_id=current_user.id,
        building_id=complaint.building_id,
        category=complaint.category,
        title=complaint.title,
        description=complaint.description,
        location=location_point,
        urgency_level=complaint.urgency_level
    )
    
    # Calculate priority score using ML
    prioritizer = ComplaintPrioritizer()
    priority_score = prioritizer.calculate_priority(complaint.dict())
    db_complaint.priority_score = priority_score
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)
    
    # Auto-assign worker if available
    await auto_assign_worker(db_complaint.id, db)
    
    return {"message": "Complaint created successfully", "complaint_id": db_complaint.id}

@router.get("/list", response_model=List[ComplaintResponse])
async def get_complaints(
    status: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(
        Complaint,
        User.first_name.label('user_first_name'),
        User.last_name.label('user_last_name'),
        func.ST_X(Complaint.location).label('longitude'),
        func.ST_Y(Complaint.location).label('latitude')
    ).join(User, Complaint.user_id == User.id)
    
    if current_user.role == "resident":
        query = query.filter(Complaint.user_id == current_user.id)
    elif current_user.role == "worker":
        query = query.filter(Complaint.assigned_worker_id == current_user.id)
    
    if status:
        query = query.filter(Complaint.status == status)
    if category:
        query = query.filter(Complaint.category == category)
    
    results = query.all()
    
    complaints = []
    for complaint, user_first, user_last, lon, lat in results:
        complaints.append(ComplaintResponse(
            id=complaint.id,
            category=complaint.category,
            title=complaint.title,
            description=complaint.description,
            latitude=lat,
            longitude=lon,
            urgency_level=complaint.urgency_level,
            status=complaint.status,
            priority_score=complaint.priority_score,
            created_at=complaint.created_at,
            user_name=f"{user_first} {user_last}",
            building_name="",  # Add building name logic
            assigned_worker_name=None  # Add worker name logic
        ))
    
    return complaints

@router.post("/{complaint_id}/update")
async def update_complaint(
    complaint_id: int,
    update: ComplaintUpdateCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    # Create update record
    db_update = ComplaintUpdate(
        complaint_id=complaint_id,
        user_id=current_user.id,
        update_text=update.update_text,
        status=update.status
    )
    db.add(db_update)
    
    # Update complaint status if provided
    if update.status:
        complaint.status = update.status
        if update.status == "resolved":
            complaint.resolved_at = datetime.utcnow()
    
    db.commit()
    return {"message": "Complaint updated successfully"}

async def auto_assign_worker(complaint_id: int, db: Session):
    """Auto-assign available worker based on category and location"""
    # Implementation for worker assignment logic
    pass
