from setuptools import setup, find_packages

setup(
    name="cvd-risk-calculator",
    version="1.0.0",
    description="CVD Risk Calculator with XGBoost and MLflow",
    author="Your Team",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0",
        "sqlalchemy==2.0.23",
        "psycopg2-binary==2.9.9",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "python-dotenv==1.0.0",
        "mlflow==2.8.0",
        "pandas==2.1.3",
        "numpy==1.24.3",
        "xgboost==2.0.0",
        "shap==0.44.0",
        "joblib==1.3.2",
    ],
    entry_points={
        "console_scripts": [
            "cvd-server=app.main:main",
        ],
    },
    python_requires=">=3.10",
)
