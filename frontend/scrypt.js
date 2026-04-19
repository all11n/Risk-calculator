/**
 * @fileoverview Основной скрипт для расчёта риска сердечно-сосудистых заболеваний.
 * Собирает данные формы, отправляет на бэкенд и отображает результаты.
 */

/**
 * Ждём полной загрузки DOM, затем вешаем обработчик на форму.
 */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('riskForm');
    const resultsDiv = document.getElementById('results');

    /**
     * Обработчик отправки формы.
     * @async
     * @param {Event} e - Событие отправки формы.
     */
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Собираем данные в формате, который ждёт бэкенд
        const formData = {
            age: parseInt(document.getElementById('age').value),
            sex: parseInt(document.getElementById('sex').value),
            smoking: parseInt(document.getElementById('smoking').value),
            cholesterol: parseFloat(document.getElementById('cholesterol').value),
            systolic_bp: parseInt(document.getElementById('systolic_bp').value),
            diastolic_bp: parseInt(document.getElementById('diastolic_bp').value),
            height: parseFloat(document.getElementById('height').value),
            weight: parseFloat(document.getElementById('weight').value),
            pulse: parseInt(document.getElementById('pulse').value),
            glucose: parseFloat(document.getElementById('glucose').value),
            diabetes: parseInt(document.getElementById('diabetes').value),
            hypertension: parseInt(document.getElementById('hypertension').value)
        };

        const submitBtn = form.querySelector('button');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = '⏳ Расчёт...';
        submitBtn.disabled = true;

        try {
            const response = await callBackend(formData);
            displayResults(response);
            resultsDiv.style.display = 'block';
            resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при расчёте риска. Попробуйте позже.');
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
});

/**
 * Отправляет POST-запрос на бэкенд для расчёта риска ССЗ.
 *
 * @async
 * @param {Object} data - Данные пользователя из формы.
 * @param {number} data.age - Возраст (18–100 лет).
 * @param {number} data.sex - Пол (0 — женский, 1 — мужской).
 * @param {number} data.smoking - Курение (0 — нет, 1 — да).
 * @param {number} data.cholesterol - Холестерин (мг/дл, 100–400).
 * @param {number} data.systolic_bp - Систолическое давление (80–200 мм рт. ст.).
 * @param {number} data.diastolic_bp - Диастолическое давление (40–130 мм рт. ст.).
 * @param {number} data.height - Рост в см (100–220).
 * @param {number} data.weight - Вес в кг (30–200).
 * @param {number} data.pulse - Пульс (40–200 уд/мин).
 * @param {number} data.glucose - Глюкоза (мг/дл, 50–400).
 * @param {number} data.diabetes - Диабет (0 — нет, 1 — да).
 * @param {number} data.hypertension - Гипертония (0 — нет, 1 — да).
 * @returns {Promise<Object>} Объект с результатами расчёта.
 * @throws {Error} Если ответ сервера не OK.
 */
async function callBackend(data) {
    const response = await fetch('http://localhost:8000/api/v1/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Ошибка сервера ${response.status}: ${errorText}`);
    }

    return await response.json();
}

/**
 * Отображает результаты расчёта на странице.
 *
 * @param {Object} data - Данные, полученные от бэкенда.
 * @param {number} data.risk_percentage - Риск в процентах (0–100).
 * @param {string} data.risk_level - Уровень риска ("Низкий", "Средний", "Высокий").
 * @param {Array<Object>} data.factors - Список факторов риска.
 * @param {number} [data.prediction_id] - ID записи в БД (опционально).
 * @param {string} [data.timestamp] - Время расчёта (опционально).
 */
function displayResults(data) {
    const riskPercent = data.risk_percentage;
    const riskLevel = data.risk_level;
    
    const totalRiskSpan = document.getElementById('totalRisk');
    totalRiskSpan.textContent = `${Math.round(riskPercent)}%`;
    
    totalRiskSpan.classList.remove('low', 'medium', 'high');
    if (riskPercent > 20) totalRiskSpan.classList.add('high');
    else if (riskPercent > 10) totalRiskSpan.classList.add('medium');
    else totalRiskSpan.classList.add('low');
    
    const riskLevelDiv = document.getElementById('riskLevel');
    riskLevelDiv.textContent = `Уровень риска: ${riskLevel}`;
    riskLevelDiv.className = `risk-level ${riskLevel.toLowerCase()}`;
    
    const factorsUl = document.getElementById('factorsUl');
    factorsUl.innerHTML = '';
    if (data.factors && data.factors.length > 0) {
        data.factors.forEach(factor => {
            const li = document.createElement('li');
            const impactSymbol = factor.impact === 'positive' ? '🔴' : '🟢';
            li.innerHTML = `${impactSymbol} ${factor.name}: ${factor.value} (вклад: ${(factor.contribution * 100).toFixed(1)}%)`;
            factorsUl.appendChild(li);
        });
    } else {
        factorsUl.innerHTML = '<li>Нет значимых факторов</li>';
    }
    
    const predictionInfo = document.getElementById('predictionInfo');
    if (data.prediction_id && data.timestamp) {
        predictionInfo.innerHTML = `ID расчёта: ${data.prediction_id} | ${new Date(data.timestamp).toLocaleString()}`;
    }
    
    drawFactorsChart(data.factors);
}

/**
 * Рисует круговую диаграмму вклада факторов риска.
 *
 * @param {Array<Object>} factors - Список факторов риска.
 * @param {string} factors[].name - Название фактора.
 * @param {number} factors[].contribution - Вклад фактора (от 0 до 1).
 * @param {string} factors[].impact - Влияние ("positive" или "negative").
 */
function drawFactorsChart(factors) {
    const canvas = document.getElementById('factorsChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Проверяем, существует ли график и есть ли у него метод destroy
    if (window.factorsChart && typeof window.factorsChart.destroy === 'function') {
        window.factorsChart.destroy();
    }
    
    if (!factors || factors.length === 0) {
        window.factorsChart = new Chart(ctx, {
            type: 'doughnut',
            data: { labels: ['Нет данных'], datasets: [{ data: [1], backgroundColor: ['#9ca3af'] }] }
        });
        return;
    }
    
    const labels = factors.map(f => f.name);
    const contributions = factors.map(f => Math.abs(f.contribution));
    const colors = factors.map(f => f.impact === 'positive' ? '#ef4444' : '#10b981');
    
    window.factorsChart = new Chart(ctx, {
        type: 'doughnut',
        data: { labels: labels, datasets: [{ data: contributions, backgroundColor: colors, borderWidth: 0 }] },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { callbacks: { label: (ctx) => `${ctx.label}: ${(ctx.raw * 100).toFixed(1)}% вклада` } }
            }
        }
    });
}
