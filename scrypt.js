// Ждём загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    // Элементы формы
    const ageSlider = document.getElementById('age');
    const ageValue = document.getElementById('ageValue');
    const form = document.getElementById('riskForm');
    const resultCard = document.getElementById('resultCard');

    // Отображение текущего значения возраста
    if (ageSlider && ageValue) {
        ageSlider.addEventListener('input', (e) => {
            ageValue.textContent = e.target.value;
        });
    }

    // Обработка отправки формы
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Собираем данные из формы
        const formData = {
            age: parseInt(document.getElementById('age').value),
            gender: document.querySelector('input[name="gender"]:checked').value,
            cholesterol: parseFloat(document.getElementById('cholesterol').value),
            systolic: parseInt(document.getElementById('systolic').value),
            diastolic: parseInt(document.getElementById('diastolic').value),
            smokes: document.getElementById('smokes').value === 'true',
            activity: document.getElementById('activity').value
        };

        // Показываем индикатор загрузки
        const submitBtn = form.querySelector('button');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = '⏳ Расчёт...';
        submitBtn.disabled = true;

        try {
            // Отправляем запрос к API (пока имитируем ответ)
            // TODO: заменить на реальный API endpoint, когда бэкенд будет готов
            const response = await mockApiCall(formData);
            
            // Отображаем результаты
            displayResults(response);
            
            // Показываем карточку с результатами
            resultCard.style.display = 'block';
            
            // Плавная прокрутка к результатам
            resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
            
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
 * Пока бэкенд не готов, используем мок-данные
 */
async function mockApiCall(data) {
    // Имитация задержки сети
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // Простая логика для демонстрации (в реальном проекте здесь будет запрос к серверу)
    const baseRisk = calculateMockRisk(data);
    
    return {
        heart_attack_risk: baseRisk * 1.2,
        stroke_risk: baseRisk * 0.9,
        heart_failure_risk: baseRisk * 1.1,
        factors: getFactorsList(data)
    };
}

/**
 * Мок-расчёт риска (временная заглушка)
 */
function calculateMockRisk(data) {
    let risk = 0.05; // базовый риск 5%
    
    if (data.age > 50) risk += (data.age - 50) * 0.005;
    if (data.gender === 'male') risk += 0.02;
    if (data.cholesterol > 5.0) risk += (data.cholesterol - 5.0) * 0.03;
    if (data.systolic > 130) risk += (data.systolic - 130) * 0.002;
    if (data.smokes) risk += 0.05;
    if (data.activity === 'low') risk += 0.03;
    
    return Math.min(risk, 0.45); // не более 45%
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
    
    if (factors.length === 0) {
        factors.push('Основные показатели в норме');
    }
    
    return factors;
}

/**
 * Отображение результатов на странице
 */
function displayResults(data) {
    // Получаем общий риск (средний по трём меткам)
    const avgRisk = (data.heart_attack_risk + data.stroke_risk + data.heart_failure_risk) / 3;
    const riskPercent = Math.round(avgRisk * 100);
    
    // Обновляем спидометр
    const gaugeFill = document.getElementById('gaugeFill');
    const gaugeValue = document.getElementById('gaugeValue');
    
    gaugeValue.textContent = `${riskPercent}%`;
    gaugeFill.style.width = `${riskPercent}%`;
    
    // Определяем цвет шкалы
    let riskLevel = 'low';
    let riskColor = '#4caf50';
    if (riskPercent > 20) {
        riskLevel = 'high';
        riskColor = '#f44336';
    } else if (riskPercent > 10) {
        riskLevel = 'medium';
        riskColor = '#ff9800';
    }
    gaugeFill.className = `gauge-fill ${riskLevel}`;
    
    // Обновляем детализацию рисков
    document.getElementById('heartAttackRisk').textContent = `${Math.round(data.heart_attack_risk * 100)}%`;
    document.getElementById('strokeRisk').textContent = `${Math.round(data.stroke_risk * 100)}%`;
    document.getElementById('heartFailureRisk').textContent = `${Math.round(data.heart_failure_risk * 100)}%`;
    
    // Применяем цвета к рискам
    applyRiskColor('heartAttackRisk', data.heart_attack_risk);
    applyRiskColor('strokeRisk', data.stroke_risk);
    applyRiskColor('heartFailureRisk', data.heart_failure_risk);
    
    // Обновляем список факторов
    const factorsUl = document.getElementById('factorsUl');
    factorsUl.innerHTML = '';
    data.factors.forEach(factor => {
        const li = document.createElement('li');
        li.textContent = factor;
        factorsUl.appendChild(li);
    });
    
    // Обновляем рекомендацию
    const recommendationText = document.getElementById('recommendationText');
    recommendationText.textContent = getRecommendation(riskPercent, data.factors);
}

/**
 * Применение цвета к элементу риска
 */
function applyRiskColor(elementId, risk) {
    const element = document.getElementById(elementId);
    const riskPercent = risk * 100;
    
    element.classList.remove('low', 'medium', 'high');
    if (riskPercent > 20) {
        element.classList.add('high');
    } else if (riskPercent > 10) {
        element.classList.add('medium');
    } else {
        element.classList.add('low');
    }
}

/**
 * Генерация рекомендации на основе риска и факторов
 */
function getRecommendation(riskPercent, factors) {
    if (riskPercent <= 10) {
        return 'Ваш риск низкий. Поддерживайте здоровый образ жизни, регулярно проходите профилактические осмотры.';
    } else if (riskPercent <= 20) {
        return 'Ваш риск средний. Рекомендуется: увеличить физическую активность, нормализовать питание, контролировать давление и холестерин.';
    } else {
        const mainFactor = factors[0] !== 'Основные показатели в норме' ? factors[0] : 'повышенный риск';
        return `Ваш риск высокий. Настоятельно рекомендуется обратиться к врачу-кардиологу. Основной фактор: ${mainFactor}. Возможно, потребуется медикаментозная профилактика.`;
    }
}
