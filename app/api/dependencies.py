from fastapi import HTTPException
from app.ml.predictor import CVDModel
from app.core.config import settings

_model_instance = None

async def get_model():
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
