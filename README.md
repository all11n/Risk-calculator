# Risk-calculator
Веб‑сервис оценки риска сердечно‑сосудистых заболеваний с использованием XGBoost и MLflow
## О проекте
Сервис позволяет оценить риск развития сердечно-сосудистых заболеваний на основе медицинских показателей пациента. В отличие от классических подходов, использующих только бинарную классификацию (есть риск / нет риска), наш проект применяет многометочную классификацию (multi-label classification) для предсказания нескольких типов рисков одновременно:
- Риск Ишемической болезни сердца
- Риск гипертензивной болезни сердца
- Риск сердечной недостаточность
- Риск болезни перикарда
- Риск опухоли сердца

Такой подход даёт более детальную картину здоровья пациента.

## Стек технологий

| Компонент | Технология |
|-----------|-----------|
| **Backend** | Python 3.9+, Flask, SQLAlchemy, Flask-JWT-Extended |
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js |
| **Machine Learning** | Python, pandas, numpy, scikit-learn, CatBoost/XGBoost, multi-label classification, SHAP |
| **MLOps / Эксперименты** | MLflow (отслеживание экспериментов, логирование моделей) |
| **База данных** | SQLite (разработка), PostgreSQL (продакшн) |
| **Система сборки** | setuptools |
| **Документация** | Sphinx (docstrings) |
| **Контроль версий** | Git, GitHub |

## Зависимости

Файл `requirements.txt`

## Запуск проекта
### Способ 1: Через Docker

``` bash 
docker-compose up --build

После запуска: 
Backend API: http://localhost:8000/docs
MLflow UI: http://localhost:5001
```
### Способ 2: Вручную
### 1. Клонирование репозитория
```bash
git clone https://github.com/ваш-username/Risk-calculator.git
cd Risk-calculator
```
### 2. Создание виртуального окружения
```bash
python3.11 -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
```
### 3. Установка зависимостей
```bash
pip install -e .
```
### 4. Запуск MLflow (отслеживание экспериментов)
```bash
mlflow ui --host 0.0.0.0 --port 5001
```
MLflow UI будет доступен по адресу: http://127.0.0.1:5001
### 5. Запуск бэкенда
```bash
cvd-server
# или
uvicorn app.main:app --reload
```
Сервер запустится по адресу: http://127.0.0.1:5000
### 6. Запуск фронтенда

Откройте файл frontend/index.html в браузере или в новой вкладке терминала

Фронтенд будет доступен: http://127.0.0.1:8000

### Способ 3: Через setuptools (установка как пакета)

Этот способ позволяет установить проект как Python-пакет и запускать его одной командой из любого места.

#### Первый раз (после клонирования):

```bash
# 1. Создать виртуальное окружение
python3.11 -m venv venv

# 2. Активировать
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

# 3. Установить проект (ОДИН РАЗ)
pip install -e .

# 4. Запустить
cvd-server
```
## Последующие запуски (уже с установленным проектом):
```bash
# 1. Активировать виртуальное окружение 
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
# 2. Запустить  
cvd-server
```
## Структура проекта
```test
Risk-calculator/
├── backend/ # Flask-приложение
│ ├── app/
│ │ ├── api/ # Эндпоинты
│ │ ├── core/ # Ядро приложения
│ │ ├── models/ # Модели БД
│ │ └── ml/ # ML модель
├── frontend/ # HTML, CSS, JS
│ ├── index.html
│ ├── scrypt.js
│ └── style.css
├── ml_service/ # Модели ML
│ ├── notebooks/ # Jupyter ноутбуки
│ ├── models/ # Сохранённые модели
│ ├── mlruns/ # MLflow эксперименты
│ └── data/ # Датасеты
├── docs/ # Sphinx-документация
├── requirements.txt
├── docker-compose.yml # Запуск всех сервисов
├── Dockerfile # Сборка backend образа
├── setup.py
├── .gitignore
├── .env.example # Пример переменных окружения
└── README.md
```
## MLflow и многометочная классификация
MLflow используется для:
Логирования гиперпараметров моделей

Отслеживания метрик (accuracy, F1-score, hamming loss)

Сохранения артефактов (моделей, графиков)

Сравнения экспериментов

Логирования SHAP-объяснений (важность признаков)

Многометочная классификация
В отличие от бинарной классификации (риск есть/нет), модель предсказывает несколько целевых меток одновременно: main
