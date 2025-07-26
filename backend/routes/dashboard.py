from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from pydantic import BaseModel
from config.database import get_db
from models.complaint import Complaint
from models.user import User
from models.building import Building
from models.utility import UtilityConsumption
from datetime import datetime, timedelta

router = APIRouter()

class DashboardStats(BaseModel):
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    critical_complaints: int
    total_buildings: int
    active_workers: int
    recent_activity: list

async def get_current_user(db: Session = Depends(get_db)):
    return db.query(User).first()

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get complaint statistics
    total_complaints = db.query(Complaint).count()
    open_complaints = db.query(Complaint).filter(Complaint.status == 'open').count()
    resolved_complaints = db.query(Complaint).filter(Complaint.status == 'resolved').count()
    critical_complaints = db.query(Complaint).filter(Complaint.urgency_level == 'critical').count()
    
    # Get building count
    total_buildings = db.query(Building).count()
    
    # Get active workers
    active_workers = db.query(User).filter(User.role == 'worker').count()
    
    # Get recent activity (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    recent_complaints = db.query(Complaint).filter(
        Complaint.created_at >= week_ago
    ).order_by(Complaint.created_at.desc()).limit(5).all()
    
    recent_activity = []
    for complaint in recent_complaints:
        recent_activity.append({
            'type': 'complaint',
            'message': f"New {complaint.category} complaint: {complaint.title}",
            'timestamp': complaint.created_at.isoformat(),
            'status': complaint.status
        })
    
    return DashboardStats(
        total_complaints=total_complaints,
        open_complaints=open_complaints,
        resolved_complaints=resolved_complaints,
        critical_complaints=critical_complaints,
        total_buildings=total_buildings,
        active_workers=active_workers,
        recent_activity=recent_activity
    )

@router.get("/complaint-trends")
async def get_complaint_trends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get complaint trends for the last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    daily_complaints = db.query(
        func.date(Complaint.created_at).label('date'),
        func.count(Complaint.id).label('count')
    ).filter(
        Complaint.created_at >= thirty_days_ago
    ).group_by(
        func.date(Complaint.created_at)
    ).order_by('date').all()
    
    trends = []
    for date, count in daily_complaints:
        trends.append({
            'date': date.strftime('%Y-%m-%d'),
            'complaints': count
        })
    
    return trends

@router.get("/category-distribution")
async def get_category_distribution(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    categories = db.query(
        Complaint.category,
        func.count(Complaint.id).label('count')
    ).group_by(Complaint.category).all()
    
    distribution = []
    for category, count in categories:
        distribution.append({
            'category': category,
            'count': count
        })
    
    return distribution
