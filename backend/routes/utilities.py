from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
from config.database import get_db
from models.utility import UtilityConsumption
from models.building import Building
from models.user import User
import pandas as pd
from prophet import Prophet

router = APIRouter()

class UtilityConsumptionCreate(BaseModel):
    building_id: int
    utility_type: str
    consumption_value: float
    unit: str
    recorded_date: date

class UtilityConsumptionResponse(BaseModel):
    id: int
    building_id: int
    utility_type: str
    consumption_value: float
    unit: str
    recorded_date: date
    building_name: str

class ConsumptionPrediction(BaseModel):
    date: str
    predicted_value: float
    lower_bound: float
    upper_bound: float

async def get_current_user(db: Session = Depends(get_db)):
    return db.query(User).first()

@router.post("/consumption/create")
async def create_consumption(
    consumption: UtilityConsumptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_consumption = UtilityConsumption(**consumption.dict())
    db.add(db_consumption)
    db.commit()
    db.refresh(db_consumption)
    
    return {"message": "Consumption data added successfully", "id": db_consumption.id}

@router.get("/consumption/list", response_model=List[UtilityConsumptionResponse])
async def get_consumption_data(
    building_id: Optional[int] = None,
    utility_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(UtilityConsumption, Building.name.label('building_name')).join(Building)
    
    if building_id:
        query = query.filter(UtilityConsumption.building_id == building_id)
    if utility_type:
        query = query.filter(UtilityConsumption.utility_type == utility_type)
    
    results = query.all()
    
    consumption_data = []
    for consumption, building_name in results:
        consumption_data.append(UtilityConsumptionResponse(
            id=consumption.id,
            building_id=consumption.building_id,
            utility_type=consumption.utility_type,
            consumption_value=consumption.consumption_value,
            unit=consumption.unit,
            recorded_date=consumption.recorded_date,
            building_name=building_name
        ))
    
    return consumption_data

@router.get("/consumption/predict/{building_id}/{utility_type}")
async def predict_consumption(
    building_id: int,
    utility_type: str,
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get historical data
    consumption_data = db.query(UtilityConsumption).filter(
        and_(
            UtilityConsumption.building_id == building_id,
            UtilityConsumption.utility_type == utility_type
        )
    ).order_by(UtilityConsumption.recorded_date).all()
    
    if len(consumption_data) < 10:
        raise HTTPException(status_code=400, detail="Insufficient data for prediction")
    
    # Prepare data for Prophet
    df = pd.DataFrame([
        {
            'ds': item.recorded_date,
            'y': item.consumption_value
        }
        for item in consumption_data
    ])
    
    # Create and fit Prophet model
    model = Prophet(daily_seasonality=True, yearly_seasonality=True)
    model.fit(df)
    
    # Make future predictions
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    
    # Get only future predictions
    future_predictions = forecast.tail(days)
    
    predictions = []
    for _, row in future_predictions.iterrows():
        predictions.append(ConsumptionPrediction(
            date=row['ds'].strftime('%Y-%m-%d'),
            predicted_value=row['yhat'],
            lower_bound=row['yhat_lower'],
            upper_bound=row['yhat_upper']
        ))
    
    return predictions

@router.get("/consumption/analytics/{building_id}")
async def get_consumption_analytics(
    building_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get consumption data for all utility types
    consumption_data = db.query(UtilityConsumption).filter(
        UtilityConsumption.building_id == building_id
    ).all()
    
    if not consumption_data:
        raise HTTPException(status_code=404, detail="No consumption data found")
    
    # Calculate analytics
    df = pd.DataFrame([
        {
            'utility_type': item.utility_type,
            'consumption_value': item.consumption_value,
            'recorded_date': item.recorded_date
        }
        for item in consumption_data
    ])
    
    analytics = {}
    for utility_type in df['utility_type'].unique():
        utility_data = df[df['utility_type'] == utility_type]
        
        analytics[utility_type] = {
            'total_consumption': utility_data['consumption_value'].sum(),
            'average_consumption': utility_data['consumption_value'].mean(),
            'max_consumption': utility_data['consumption_value'].max(),
            'min_consumption': utility_data['consumption_value'].min(),
            'trend': 'increasing' if utility_data['consumption_value'].iloc[-1] > utility_data['consumption_value'].iloc[0] else 'decreasing'
        }
    
    return analytics
