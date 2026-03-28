import numpy as np
from typing import Dict, Any, Tuple, List
from app.core.config import settings

class CVDModel:
    def __init__(self, mlflow_uri: str = None, model_name: str = None, model_stage: str = "Production"):
        self.mlflow_uri = mlflow_uri or settings.MLFLOW_TRACKING_URI
        self.model_name = model_name or settings.MLFLOW_MODEL_NAME
        self.model_stage = model_stage or settings.MLFLOW_MODEL_STAGE
        self.model = None
        self.feature_names = [
            'age', 'sex', 'smoking', 'cholesterol', 'systolic_bp',
            'diastolic_bp', 'height', 'weight', 'pulse', 'glucose',
            'diabetes', 'hypertension'
        ]
        self.load_model()
    
    def load_model(self):
        try:
            print(f"Loading model from MLflow: {self.model_name}/{self.model_stage}")
            print("Note: Using dummy model. Data Scientist will replace this.")
            self.model = "dummy_model"
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def preprocess_input(self, data: Dict[str, Any]) -> np.ndarray:
        features = []
        for feature in self.feature_names:
            features.append(data.get(feature, 0))
        return np.array(features).reshape(1, -1)
    
    def predict(self, data: Dict[str, Any]) -> Tuple[float, List[Dict]]:
        features = self.preprocess_input(data)
        
        # Dummy prediction (random number between 0 and 0.5)
        probability = np.random.random() * 0.5
        
        factors = []
        for i, name in enumerate(self.feature_names):
            contribution = (np.random.random() - 0.5) * 0.1
            factors.append({
                "name": name,
                "value": data.get(name, 0),
                "contribution": float(contribution),
                "impact": "positive" if contribution > 0 else "negative"
            })
        
        return float(probability), factors
    
    def get_model_info(self) -> Dict:
        return {
            "model_name": self.model_name,
            "model_stage": self.model_stage,
            "mlflow_uri": self.mlflow_uri,
            "status": "loaded" if self.model else "not_loaded"
        }
