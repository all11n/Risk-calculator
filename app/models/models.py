"""
Модуль SQLAlchemy-моделей для базы данных.

Содержит модель Prediction для хранения результатов расчёта риска ССЗ.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Prediction(Base):
        """
    Модель для хранения предсказаний риска сердечно-сосудистых заболеваний.

    Сохраняет входные данные пользователя, результаты расчёта и временную метку.
    Используется для ведения истории расчётов и аналитики.

    Attributes:
        id (int): Уникальный идентификатор записи (первичный ключ).
        timestamp (datetime): Время создания записи (автоматически).
        input_data (dict): JSON с входными данными пользователя.
        risk_percentage (float): Риск в процентах (0–100).
        risk_probability (float): Вероятность риска (0–1).
        risk_level (str): Уровень риска ("Низкий", "Средний", "Высокий").
        shap_factors (list): JSON со списком факторов риска и их вкладом.

    Example:
        >>> prediction = Prediction(
        ...     input_data={"age": 55, "sex": 1, "smoking": 1},
        ...     risk_percentage=23.5,
        ...     risk_probability=0.235,
        ...     risk_level="Средний",
        ...     shap_factors=[{"name": "age", "contribution": 0.12}]
        ... )
        >>> db.add(prediction)
        >>> db.commit()
        >>> print(prediction.id)
        1
    """
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    input_data = Column(JSON)
    risk_percentage = Column(Float)
    risk_probability = Column(Float)
    risk_level = Column(String)
    shap_factors = Column(JSON)
