from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    input_data = Column(JSON)
    risk_percentage = Column(Float)
    risk_probability = Column(Float)
    risk_level = Column(String)
    shap_factors = Column(JSON)
