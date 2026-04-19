#!/usr/bin/env python3
"""
Простой генератор Sphinx-документации.
Запуск: python3 make_docs.py
"""
import os, sys
from pathlib import Path

# === НАСТРОЙКИ ===
ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
SRC = DOCS / "source"

# === МИНИМАЛЬНЫЙ conf.py ===
CONF = '''import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

project, copyright, author = "CVD Risk Calculator", "2026", "Team"
release, language = "1.0.0", "ru"

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "myst_parser"]
napoleon_google_docstring = True
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
html_theme = "sphinx_rtd_theme"
'''

# === ГЛАВНАЯ СТРАНИЦА ===
INDEX = '''.. CVD Risk Calculator docs

CVD Risk Calculator
===================

.. toctree::
   :maxdepth: 2
   :caption: Содержание:

   backend/api
   ml/predictor
   frontend/overview

Запуск
------
.. code-block:: bash

   pip install -r requirements.txt
   uvicorn app.main:app --reload
'''

# === ШАБЛОНЫ ===
def rst_auto(module: str) -> str:
    title = module.replace('_', ' ').replace('.', ' ').title()
    return f"""{title}
{'=' * len(title)}

.. automodule:: {module}
   :members:
   :undoc-members:
   :show-inheritance:
"""

def frontend_md() -> str:
    # Используем \\``` чтобы не ломать Python-строку
    return """# Frontend

## Структура

::
    frontend/
    ├── index.html
    ├── scrypt.js
    └── style.css

## Функции

### callBackend(data)
Отправляет POST на /api/v1/predict.

**Параметры:**
- `data` (Object): Данные пользователя

**Возвращает:** Promise с результатами

### displayResults(data)
Показывает риск и факторы на странице.

## Запуск локально

.. code-block:: bash

    cd frontend && python3 -m http.server 3000

"""

# === ОСНОВНАЯ ЛОГИКА ===
def main():
    print("🔧 Генерация документации...")
    
    # Создаём папки
    for d in [SRC/"backend", SRC/"ml", SRC/"frontend"]:
        d.mkdir(parents=True, exist_ok=True)
    
    # Пишем файлы
    (SRC/"conf.py").write_text(CONF, encoding="utf-8")
    (SRC/"index.rst").write_text(INDEX, encoding="utf-8")
    (DOCS/"requirements.txt").write_text(
        "sphinx==7.2.6\nsphinx-rtd-theme==2.0.0\nmyst-parser==2.0.0\n",
        encoding="utf-8"
    )
    
    # Backend (если файлы есть)
    api_dir = ROOT/"app/api"
    if api_dir.exists():
        for f in api_dir.glob("*.py"):
            if f.name.startswith("_"): continue
            mod = f"app.api.{f.stem}"
            (SRC/"backend"/f"{f.stem}.rst").write_text(rst_auto(mod), encoding="utf-8")
            print(f"✅ backend/{f.stem}.rst")
    
    # ML
    ml_file = ROOT/"app/ml/predictor.py"
    if ml_file.exists():
        (SRC/"ml/predictor.rst").write_text(
            rst_auto("app.ml.predictor"), encoding="utf-8"
        )
        print("✅ ml/predictor.rst")
    
    # Frontend
    (SRC/"frontend/overview.md").write_text(frontend_md(), encoding="utf-8")
    print("✅ frontend/overview.md")
    
    print("\n🎉 Готово!")
    print("1. cd docs && pip3 install -r requirements.txt --user")
    print("2. sphinx-build source build/html")
    print("3. Открой docs/build/html/index.html")

if __name__ == "__main__":
    main()