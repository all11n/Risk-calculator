// Ждём загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('riskForm');
    const resultsDiv = document.getElementById('results');
    
    let riskChart = null;
    let factorsChart = null;

    // Обработка отправки формы
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Собираем данные из формы
        const formData = {
            age: parseInt(document.getElementById('age').value),
            gender: document.getElementById('gender').value,
            cholesterol: parseFloat(document.getElementById('cholesterol').value),
            systolic: parseInt(document.getElementById('systolic').value),
            smokes: document.getElementById('smokes').value === 'true',
            activity: document.getElementById('activity').value
        };

        // Показываем индикатор загрузки
        const submitBtn = form.querySelector('button');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = '⏳ Расчёт...';
        submitBtn.disabled = true;

        try {
            // Имитация запроса к API (пока бэкенд не готов)
            const response = await mockApiCall(formData);
            
            // Отображаем результаты
            displayResults(response);
            
            // Показываем блок с результатами
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
 * Имитация API-запроса (временная заглушка)
 */
async function mockApiCall(data) {
    await new Promise(resolve => setTimeout(resolve, 800));
    
    const baseRisk = calculateMockRisk(data);
    
    return {
        heart_attack_risk: Math.min(baseRisk * 1.2, 0.45),
        stroke_risk: Math.min(baseRisk * 0.9, 0.45),
        heart_failure_risk: Math.min(baseRisk * 1.1, 0.45),
        factors: getFactorsList(data)
    };
}

/**
 * Мок-расчёт риска
 */
function calculateMockRisk(data) {
    let risk = 0.05;
    
    if (data.age > 50) risk += (data.age - 50) * 0.005;
    if (data.gender === 'male') risk += 0.02;
    if (data.cholesterol > 5.0) risk += (data.cholesterol - 5.0) * 0.03;
    if (data.systolic > 130) risk += (data.systolic - 130) * 0.002;
    if (data.smokes) risk += 0.05;
    if (data.activity === 'low') risk += 0.03;
    
    return Math.min(risk, 0.45);
}

/**
 * Получение списка факторов риска
 */
function getFactorsList(data) {
    const factors = [];
    
    if (data.smokes) factors.push('Курение');
    if (data.age > 60) factors.push('Возраст (>60 лет)');
    if (data.cholesterol > 6.0) factors.push('Высокий холестерин');
    if (data.systolic > 140) factors.push('Повышенное давление');
    if (data.activity === 'low') factors.push('Низкая физическая активность');
    if (data.gender === 'male' && data.age > 45) factors.push('Мужской пол + возраст >45');
    
    if (factors.length === 0) factors.push('Основные показатели в норме');
    
    return factors;
}

/**
 * Отображение результатов
 */
function displayResults(data) {
    const avgRisk = (data.heart_attack_risk + data.stroke_risk + data.heart_failure_risk) / 3;
    const riskPercent = Math.round(avgRisk * 100);
    
    // Обновляем общий риск
    const totalRiskSpan = document.getElementById('totalRisk');
    totalRiskSpan.textContent = `${riskPercent}%`;
    
    // Определяем класс цвета
    totalRiskSpan.classList.remove('low', 'medium', 'high');
    if (riskPercent > 20) {
        totalRiskSpan.classList.add('high');
    } else if (riskPercent > 10) {
        totalRiskSpan.classList.add('medium');
    } else {
        totalRiskSpan.classList.add('low');
    }
    
    // Обновляем список факторов
    const factorsUl = document.getElementById('factorsUl');
    factorsUl.innerHTML = '';
    data.factors.forEach(factor => {
        const li = document.createElement('li');
        li.textContent = factor;
        factorsUl.appendChild(li);
    });
    
    // Отрисовываем графики
    drawRiskChart(data);
    drawFactorsChart(data.factors);
}

/**
 * График рисков по заболеваниям
 */
function drawRiskChart(data) {
    const ctx = document.getElementById('riskChart').getContext('2d');
    
    // Удаляем старый график, если есть
    if (window.riskChart) window.riskChart.destroy();
    
    window.riskChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Инфаркт', 'Инсульт', 'Сердечная недостаточность'],
            datasets: [{
                label: 'Риск (%)',
                data: [
                    Math.round(data.heart_attack_risk * 100),
                    Math.round(data.stroke_risk * 100),
                    Math.round(data.heart_failure_risk * 100)
                ],
                backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6'],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'top' },
                tooltip: { callbacks: { label: (ctx) => `${ctx.raw}%` } }
            },
            scales: {
                y: { beginAtZero: true, max: 50, title: { display: true, text: 'Риск (%)' } }
            }
        }
    });
}

/**
 * Круговая диаграмма факторов риска
 */
function drawFactorsChart(factors) {
    const ctx = document.getElementById('factorsChart').getContext('2d');
    
    if (window.factorsChart) window.factorsChart.destroy();
    
    // Считаем, сколько раз встречается каждый фактор (упрощённо)
    const factorCount = {};
    factors.forEach(f => { factorCount[f] = (factorCount[f] || 0) + 1; });
    
    window.factorsChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(factorCount),
            datasets: [{
                data: Object.values(factorCount),
                backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { callbacks: { label: (ctx) => `${ctx.label}: ${ctx.raw} фактор(а)` } }
            }
        }
    });
}
