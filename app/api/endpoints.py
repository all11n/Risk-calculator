"""
Модуль API для расчёта риска сердечно-сосудистых заболеваний.

Содержит эндпоинты:
- POST /predict - расчёт риска
- GET /health - проверка состояния сервиса
"""
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
    """
    Рассчитывает 10-летний риск сердечно-сосудистых заболеваний.

    Принимает данные пользователя, вызывает ML-модель, сохраняет результат в БД
    и возвращает рассчитанный риск и факторы влияния.

    Args:
        request (CVDRequest): Входные данные пользователя (возраст, пол, давление и т.д.).
        db (Session): Сессия базы данных (внедряется через Depends).
        model (CVDModel): Загруженная ML-модель (внедряется через Depends).

    Returns:
        CVDResponse: Объект с результатами расчёта:
            - risk_percentage: риск в процентах
            - risk_probability: вероятность (0-1)
            - risk_level: уровень риска ("Низкий", "Средний", "Высокий")
            - factors: список факторов с вкладом
            - prediction_id: ID записи в БД
            - timestamp: время расчёта

    Raises:
        HTTPException: Если модель недоступна или произошла ошибка предсказания.

    Example:
        >>> request = CVDRequest(age=55, sex=1, smoking=1, ...)
        >>> response = await predict_risk(request, db, model)
        >>> print(response.risk_percentage)
        23.5
    """
    # Получаем предсказание от модели
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
    """
    Проверяет состояние сервиса (health check).

    Проверяет подключение к базе данных и доступность ML-модели.

    Args:
        db (Session): Сессия базы данных (внедряется через Depends).

    Returns:
        HealthResponse: Объект со статусами:
            - status: "healthy" или "unhealthy"
            - database: "connected" или "disconnected"
            - model: "loaded", "unavailable" или "unknown"
            - timestamp: время проверки

    Example:
        >>> response = await health_check(db)
        >>> print(response.status)
        'healthy'
    """
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
