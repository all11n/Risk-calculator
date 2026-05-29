"""
Модуль для загрузки и использования ML-модели сердечно-сосудистых заболеваний.

Содержит класс CVDModel, который:
- Загружает модель из MLflow
- Преобразует входные данные в формат для модели
- Выполняет предсказания
- Возвращает факторы риска с их вкладом
"""
import numpy as np
from typing import Dict, Any, Tuple, List
from app.core.config import settings


class CVDModel:
    """
    Класс для работы с ML-моделью сердечно-сосудистых заболеваний.

    Обеспечивает загрузку модели из MLflow, предобработку входных данных,
    выполнение предсказаний и возврат интерпретируемых факторов риска.

    Attributes:
        mlflow_uri (str): URI MLflow tracking server.
        model_name (str): Имя модели в MLflow.
        model_stage (str): Стадия модели ("Production", "Staging", "Archived").
        model (Any): Загруженная ML-модель (заглушка или реальная).
        feature_names (List[str]): Список названий признаков в порядке для модели.

    Example:
        >>> model = CVDModel()
        >>> data = {"age": 55, "sex": 1, "smoking": 1, ...}
        >>> probability, factors = model.predict(data)
        >>> print(f"Риск: {probability * 100:.1f}%")
    """
    def __init__(self, mlflow_uri: str = None, model_name: str = None, model_stage: str = "Production"):
        """
        Инициализирует экземпляр CVDModel.

        Args:
            mlflow_uri (str, optional): URI MLflow tracking server.
                По умолчанию берется из settings.MLFLOW_TRACKING_URI.
            model_name (str, optional): Имя модели в MLflow.
                По умолчанию берется из settings.MLFLOW_MODEL_NAME.
            model_stage (str, optional): Стадия модели.
                По умолчанию "Production" или из settings.MLFLOW_MODEL_STAGE.

        Example:
            >>> model = CVDModel(
            ...     mlflow_uri="http://localhost:5000",
            ...     model_name="cvd_risk_model",
            ...     model_stage="Production"
            ... )
        """
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
        """
        Загружает модель из MLflow.

        В текущей реализации используется заглушка.
        При подключении реального MLflow сервера здесь будет реальная загрузка.

        Returns:
            None

        Raises:
            Exception: Если модель не удалось загрузить.

        Example:
            >>> model = CVDModel()
            >>> model.load_model()  # Модель загружена
        """
        try:
            print(f"Loading model from MLflow: {self.model_name}/{self.model_stage}")
            print("Note: Using dummy model. Data Scientist will replace this.")
            self.model = "dummy_model"
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def preprocess_input(self, data: Dict[str, Any]) -> np.ndarray:
        """
        Преобразует входные данные в формат для модели.

        Извлекает признаки из словаря в порядке self.feature_names
        и преобразует их в numpy-массив формы (1, n_features).

        Args:
            data (Dict[str, Any]): Словарь с данными пользователя.
                Должен содержать все ключи из self.feature_names.

        Returns:
            np.ndarray: Массив признаков формы (1, n_features) для модели.

        Example:
            >>> data = {"age": 55, "sex": 1, "smoking": 1, ...}
            >>> features = model.preprocess_input(data)
            >>> features.shape
            (1, 12)
        """
        features = []
        for feature in self.feature_names:
            features.append(data.get(feature, 0))
        return np.array(features).reshape(1, -1)
    
    def predict(self, data: Dict[str, Any]) -> Tuple[float, List[Dict]]:
        """
        Выполняет предсказание риска на основе входных данных.

        Args:
            data (Dict[str, Any]): Словарь с данными пользователя.
                Должен содержать все ключи из self.feature_names.

        Returns:
            Tuple[float, List[Dict]]:
                - probability (float): Вероятность риска (0-1).
                - factors (List[Dict]): Список факторов с вкладом в риск.
                    Каждый фактор содержит:
                    - name (str): Название признака.
                    - value (Any): Значение признака.
                    - contribution (float): Вклад в риск (положительный или отрицательный).
                    - impact (str): "positive" (увеличивает риск) или "negative".

        Example:
            >>> data = {"age": 55, "sex": 1, "smoking": 1, ...}
            >>> probability, factors = model.predict(data)
            >>> print(f"Риск: {probability * 100:.1f}%")
            Риск: 23.5%
            >>> print(factors[0])
            {'name': 'age', 'value': 55, 'contribution': 0.12, 'impact': 'positive'}
        """
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
        """
        Возвращает информацию о загруженной модели.

        Returns:
            Dict: Словарь с информацией о модели:
                - model_name (str): Имя модели.
                - model_stage (str): Стадия модели.
                - mlflow_uri (str): URI MLflow сервера.
                - status (str): Статус загрузки ("loaded" или "not_loaded").

        Example:
            >>> info = model.get_model_info()
            >>> print(info['model_name'])
            'cvd_risk_model'
        """
        return {
            "model_name": self.model_name,
            "model_stage": self.model_stage,
            "mlflow_uri": self.mlflow_uri,
            "status": "loaded" if self.model else "not_loaded"
        }
