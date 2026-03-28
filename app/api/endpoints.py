from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.api.schemas import CVDRequest, CVDResponse, HealthResponse
from app.models.models import Prediction
from app.core.database import get_db
from app.api.dependencies import get_model
from app.ml.predictor import CVDModel

router = APIRouter()

@router.post("/predict", response_model=CVDResponse)
async def predict_risk(
    request: CVDRequest,
    db: Session = Depends(get_db),
    model: CVDModel = Depends(get_model)
):
    probability, shap_factors = model.predict(request.dict())
    risk_percentage = probability * 100
    
    if risk_percentage < 10:
        risk_level = "Низкий"
    elif risk_percentage < 20:
        risk_level = "Средний"
    else:
        risk_level = "Высокий"
    
    prediction = Prediction(
        input_data=request.dict(),
        risk_percentage=risk_percentage,
        risk_probability=probability,
        risk_level=risk_level,
        shap_factors=shap_factors
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    return CVDResponse(
        risk_percentage=risk_percentage,
        risk_probability=probability,
        risk_level=risk_level,
        factors=shap_factors,
        prediction_id=prediction.id,
        timestamp=prediction.timestamp
    )

@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    db_status = "disconnected"
    try:
        db.execute("SELECT 1")
        db_status = "connected"
    except:
        pass
    
    model_status = "unknown"
    try:
        model = await get_model()
        if model:
            model_status = "loaded"
    except:
        model_status = "unavailable"
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        database=db_status,
        model=model_status,
        timestamp=datetime.now()
    )
