"""
Модуль Pydantic-схем для валидации данных API.

Содержит модели запросов и ответов для эндпоинтов:
- CVDRequest: входные данные для расчёта риска
- CVDResponse: результат расчёта риска
- HealthResponse: статус сервиса
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime


class CVDRequest(BaseModel):
    """
    Схема запроса для расчёта риска сердечно-сосудистых заболеваний.

    Содержит все медицинские параметры пользователя с валидацией диапазонов.

    Attributes:
        age (int): Возраст в годах (18–100).
        sex (int): Пол (0 — женский, 1 — мужской).
        smoking (int): Курение (0 — нет, 1 — да).
        cholesterol (float): Холестерин (мг/дл, 100–400).
        systolic_bp (int): Систолическое давление (мм рт. ст., 80–200).
        diastolic_bp (int): Диастолическое давление (мм рт. ст., 40–130).
        height (float): Рост в см (100–220).
        weight (float): Вес в кг (30–200).
        pulse (int): Пульс (уд/мин, 40–200).
        glucose (float): Глюкоза (мг/дл, 50–400).
        diabetes (int): Диабет (0 — нет, 1 — да).
        hypertension (int): Гипертония (0 — нет, 1 — да).

    Example:
        >>> request = CVDRequest(
        ...     age=55,
        ...     sex=1,
        ...     smoking=1,
        ...     cholesterol=220,
        ...     systolic_bp=145,
        ...     diastolic_bp=85,
        ...     height=175,
        ...     weight=80,
        ...     pulse=72,
        ...     glucose=95,
        ...     diabetes=0,
        ...     hypertension=1
        ... )
    """
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
    """
    Схема ответа с результатами расчёта риска.

    Attributes:
        risk_percentage (float): Риск в процентах (0–100).
        risk_probability (float): Вероятность риска (0–1).
        risk_level (str): Уровень риска ("Низкий", "Средний", "Высокий").
        factors (List[Dict[str, Any]]): Список факторов риска с вкладом.
        prediction_id (int): ID записи в базе данных.
        timestamp (datetime): Время расчёта.

    Example:
        >>> response = CVDResponse(
        ...     risk_percentage=23.5,
        ...     risk_probability=0.235,
        ...     risk_level="Средний",
        ...     factors=[{"name": "age", "value": 55, "contribution": 0.12}],
        ...     prediction_id=123,
        ...     timestamp=datetime.now()
        ... )
    """
    risk_percentage: float
    risk_probability: float
    risk_level: str
    factors: List[Dict[str, Any]]
    prediction_id: int
    timestamp: datetime

class HealthResponse(BaseModel):
    """
    Схема ответа для проверки состояния сервиса (health check).

    Attributes:
        status (str): Общий статус ("healthy" или "unhealthy").
        database (str): Статус БД ("connected" или "disconnected").
        model (str): Статус модели ("loaded", "unavailable" или "unknown").
        timestamp (datetime): Время проверки.

    Example:
        >>> response = HealthResponse(
        ...     status="healthy",
        ...     database="connected",
        ...     model="loaded",
        ...     timestamp=datetime.now()
        ... )
    """
    status: str
    database: str
    model: str
    timestamp: datetime
