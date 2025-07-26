// Calculadora Avançada - JS
const display = document.getElementById('display');
const historyList = document.getElementById('history-list');
let current = '';
let operator = '';
let operand = '';
let history = [];

function renderDisplay(value) {
    display.textContent = value || '0';
}
function renderHistory() {
    historyList.innerHTML = '';
    history.slice().reverse().forEach(item => {
        const div = document.createElement('div');
        div.className = 'history-item';
        div.innerHTML = `<div>${item.expr}</div><div>= <b>${item.result}</b></div><span class="time">${item.time}</span>`;
        historyList.appendChild(div);
    });
}
function addToHistory(expr, result) {
    const now = new Date();
    const time = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    history.push({ expr, result, time });
    renderHistory();
}
function clearAll() {
    current = '';
    operator = '';
    operand = '';
    renderDisplay('');
}
function handleNumber(num) {
    if (current.length >= 12) return;
    current += num;
    renderDisplay(current);
}
function handleOperator(op) {
    if (current === '' && op !== '-') return;
    if (operator && operand !== '') {
        handleEqual();
    }
    operator = op;
    operand = current;
    current = '';
}
function handleEqual() {
    if (!operator || operand === '' || current === '') return;
    let expr = `${operand} ${operator} ${current}`;
    let result = '';
    try {
        let a = parseFloat(operand);
        let b = parseFloat(current);
        switch (operator) {
            case '+': result = a + b; break;
            case '-': result = a - b; break;
            case '×': result = a * b; break;
            case '÷': result = b !== 0 ? a / b : 'Erro'; break;
            case '%': result = a % b; break;
        }
        if (typeof result === 'number' && !isNaN(result)) result = result.toString();
    } catch {
        result = 'Erro';
    }
    renderDisplay(result);
    addToHistory(expr, result);
    current = result;
    operator = '';
    operand = '';
}
function handleClear() {
    clearAll();
}
function handleInvert() {
    if (current) {
        current = (parseFloat(current) * -1).toString();
        renderDisplay(current);
    }
}
function handlePercent() {
    if (current) {
        current = (parseFloat(current) / 100).toString();
        renderDisplay(current);
    }
}
function handleDot() {
    if (!current.includes('.')) {
        current += current ? '.' : '0.';
        renderDisplay(current);
    }
}
document.querySelectorAll('.btn.number').forEach(btn => {
    btn.onclick = () => handleNumber(btn.textContent);
});
document.querySelector('.btn.zero').onclick = () => handleNumber('0');
document.querySelector('.btn.add').onclick = () => handleOperator('+');
document.querySelector('.btn.subtract').onclick = () => handleOperator('-');
document.querySelector('.btn.multiply').onclick = () => handleOperator('×');
document.querySelector('.btn.divide').onclick = () => handleOperator('÷');
document.querySelector('.btn.percent').onclick = () => handleOperator('%');
document.querySelector('.btn.equal').onclick = () => handleEqual();
document.querySelector('.btn.clear').onclick = () => handleClear();
document.querySelector('.btn.invert').onclick = () => handleInvert();
document.querySelector('.btn.dot').onclick = () => handleDot();
document.querySelector('.btn.clear-history').onclick = () => {
    history = [];
    renderHistory();
};
window.onload = () => {
    clearAll();
    renderHistory();
};
