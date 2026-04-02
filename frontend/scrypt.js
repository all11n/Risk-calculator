// Ждём загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('riskForm');
    const resultsDiv = document.getElementById('results');

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
 * Запрос к бэкенду
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
 * Отображение результатов
 */
function displayResults(data) {
    // Общий риск
    const riskPercent = data.risk_percentage;
    const riskLevel = data.risk_level;
    
    const totalRiskSpan = document.getElementById('totalRisk');
    totalRiskSpan.textContent = `${Math.round(riskPercent)}%`;
    
    // Цвет риска
    totalRiskSpan.classList.remove('low', 'medium', 'high');
    if (riskPercent > 20) totalRiskSpan.classList.add('high');
    else if (riskPercent > 10) totalRiskSpan.classList.add('medium');
    else totalRiskSpan.classList.add('low');
    
    // Уровень риска
    const riskLevelDiv = document.getElementById('riskLevel');
    riskLevelDiv.textContent = `Уровень риска: ${riskLevel}`;
    riskLevelDiv.className = `risk-level ${riskLevel.toLowerCase()}`;
    
    // Список факторов
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
    
    // Информация о предсказании
    const predictionInfo = document.getElementById('predictionInfo');
    if (data.prediction_id && data.timestamp) {
        predictionInfo.innerHTML = `ID расчёта: ${data.prediction_id} | ${new Date(data.timestamp).toLocaleString()}`;
    }
    
    // Рисуем круговую диаграмму факторов
    drawFactorsChart(data.factors);
}

/**
 * Круговая диаграмма вклада факторов
 */
function drawFactorsChart(factors) {
    const ctx = document.getElementById('factorsChart').getContext('2d');
    if (window.factorsChart) window.factorsChart.destroy();
    
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
