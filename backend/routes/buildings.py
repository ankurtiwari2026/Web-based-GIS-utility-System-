from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import List
from config.database import get_db
from models.building import Building
from models.user import User

router = APIRouter()

class BuildingResponse(BaseModel):
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    building_type: str

class BuildingCreate(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    building_type: str

async def get_current_user(db: Session = Depends(get_db)):
    # This should be imported from main.py or auth
    # For now, return a dummy user
    return db.query(User).first()

@router.get("/list", response_model=List[BuildingResponse])
async def get_buildings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    buildings = db.query(
        Building,
        func.ST_X(Building.location).label('longitude'),
        func.ST_Y(Building.location).label('latitude')
    ).all()
    
    result = []
    for building, lon, lat in buildings:
        result.append(BuildingResponse(
            id=building.id,
            name=building.name,
            address=building.address,
            latitude=lat,
            longitude=lon,
            building_type=building.building_type
        ))
    
    return result

@router.post("/create", response_model=dict)
async def create_building(
    building: BuildingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    location_point = func.ST_GeomFromText(f'POINT({building.longitude} {building.latitude})', 4326)
    
    db_building = Building(
        name=building.name,
        address=building.address,
        location=location_point,
        building_type=building.building_type
    )
    
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    
    return {"message": "Building created successfully", "building_id": db_building.id}
