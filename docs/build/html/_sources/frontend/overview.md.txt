# Frontend

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

