"""
Модуль для работы с ML-моделью сердечно-сосудистых заболеваний.
Обеспечивает ленивую загрузку и кеширование экземпляра модели.
"""
from fastapi import HTTPException
from app.ml.predictor import CVDModel
from app.core.config import settings

_model_instance = None


async def get_model():
    """
    Возвращает экземпляр модели CVDModel (ленивая загрузка с кешированием).

    При первом вызове создаёт и кеширует экземпляр модели.
    При последующих вызовах возвращает уже созданный экземпляр.

    Returns:
        CVDModel: Загруженная и инициализированная модель.

    Raises:
        HTTPException: Если модель не удалось загрузить (статус 503).

    Example:
        >>> model = await get_model()
        >>> risk = await model.predict(features)
    """
    global _model_instance
    if _model_instance is None:
        try:
            _model_instance = CVDModel(
                mlflow_uri=settings.MLFLOW_TRACKING_URI,
                model_name=settings.MLFLOW_MODEL_NAME,
                model_stage=settings.MLFLOW_MODEL_STAGE
            )
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Model not available: {str(e)}"
            )
    return _model_instance
