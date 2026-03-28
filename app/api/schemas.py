from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class CVDRequest(BaseModel):
    age: int = Field(..., ge=18, le=100)
    sex: int = Field(..., ge=0, le=1)
    smoking: int = Field(..., ge=0, le=1)
    cholesterol: float = Field(..., ge=100, le=400)
    systolic_bp: int = Field(..., ge=80, le=200)
    diastolic_bp: int = Field(..., ge=40, le=130)
    height: float = Field(..., ge=100, le=220)
    weight: float = Field(..., ge=30, le=200)
    pulse: int = Field(..., ge=40, le=200)
    glucose: float = Field(..., ge=50, le=400)
    diabetes: int = Field(..., ge=0, le=1)
    hypertension: int = Field(..., ge=0, le=1)

class CVDResponse(BaseModel):
    risk_percentage: float
    risk_probability: float
    risk_level: str
    factors: List[Dict[str, Any]]
    prediction_id: int
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    database: str
    model: str
    timestamp: datetime
