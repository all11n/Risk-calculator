import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

project, copyright, author = "CVD Risk Calculator", "2026", "Team"
release, language = "1.0.0", "ru"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "myst_parser"]
napoleon_google_docstring = True
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
html_theme = "sphinx_rtd_theme"
autodoc_mock_imports = [
    "fastapi", "uvicorn", "sqlalchemy", "psycopg2",
    "pydantic", "pydantic_settings", "dotenv",
    "mlflow", "pandas", "numpy", "xgboost", "shap", "joblib",
    "app.models", "app.core.database"
]
nitpicky = False
suppress_warnings = ["autodoc.import_object"]