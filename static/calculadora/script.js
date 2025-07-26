// Calculadora Avançada - JS
const expressionDisplay = document.getElementById('expression-display');
const resultDisplay = document.getElementById('result-display');
const historyList = document.getElementById('history-list');
const loginModal = document.getElementById('login-modal');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const loginEmail = document.getElementById('login-email');
const loginSenha = document.getElementById('login-senha');
const loginError = document.getElementById('login-error');
const registerError = document.getElementById('register-error');
const logoutBar = document.getElementById('logout-bar');
const logoutBtn = document.getElementById('logout-btn');
const userInfo = document.getElementById('user-info');
const showRegisterLink = document.getElementById('show-register');
const showLoginLink = document.getElementById('show-login');

let current = null;         // Número atual sendo digitado
let operator = null;        // Operador atual (+, -, ×, ÷)
let operands = [];        // Array para armazenar múltiplos operandos
let operators = [];        // Array para armazenar múltiplos operadores
let history = [];         // Histórico de operações
let user = null;          // Dados do usuário logado
let accessToken = null;   // Token de acesso JWT
let refreshToken = null;  // Token de refresh JWT

const API_BASE = '/api';

function showLoginModal(show = true) {
    loginModal.style.display = show ? 'flex' : 'none';
}
function showLogoutBar(show = true) {
    logoutBar.style.display = show ? 'block' : 'none';
}
function setUserInfo(userObj) {
    if (userObj) {
        userInfo.textContent = `Bem-vindo, ${userObj.nome || userObj.username || userObj.email}`;
        showLogoutBar(true);
    } else {
        userInfo.textContent = '';
        showLogoutBar(false);
    }
}
function saveTokens(access, refresh) {
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    accessToken = access;
    refreshToken = refresh;
}
function clearTokens() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    accessToken = null;
    refreshToken = null;
}
function loadTokens() {
    accessToken = localStorage.getItem('accessToken');
    refreshToken = localStorage.getItem('refreshToken');
}
async function apiRequest(url, options = {}) {
    if (!options.headers) options.headers = {};
    if (accessToken) {
        options.headers['Authorization'] = 'Bearer ' + accessToken;
    }
    if (options.body && typeof options.body !== 'string') {
        options.body = JSON.stringify(options.body);
        options.headers['Content-Type'] = 'application/json';
    }
    let resp = await fetch(url, options);
    // Tenta refresh se 401
    if (resp.status === 401 && refreshToken && url !== `${API_BASE}/auth/token/refresh/`) {
        let ok = await tryRefreshToken();
        if (ok) {
            options.headers['Authorization'] = 'Bearer ' + accessToken;
            resp = await fetch(url, options);
        } else {
            logout();
            throw new Error('Sessão expirada. Faça login novamente.');
        }
    }
    return resp;
}
async function tryRefreshToken() {
    if (!refreshToken) return false;
    let resp = await fetch(`${API_BASE}/auth/token/refresh/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({refresh: refreshToken})
    });
    if (resp.ok) {
        let data = await resp.json();
        if (data.access) {
            saveTokens(data.access, refreshToken);
            return true;
        }
    }
    return false;
}
function logout() {
    clearTokens();
    user = null;
    setUserInfo(null);
    showLoginModal(true);
    clearAll();
    history = [];
    renderHistory();
}

function renderDisplay() {
    // Atualiza o display da expressão
    let expression = '';
    
    // Adiciona os operandos e operadores à expressão
    operands.forEach((operand, index) => {
        expression += operand + ' ';
        if (operators[index]) {
            expression += operators[index] + ' ';
        }
    });
    
    // Adiciona o operador atual, se houver
    if (operator) {
        expression += operator + ' ';
    }
    
    // Adiciona o número atual, se houver
    if (current !== null) {
        expression += current;
    }
    
    // Atualiza os displays
    expressionDisplay.textContent = expression.trim() || '\u00A0'; // Usa espaço em branco se não houver expressão
    resultDisplay.textContent = current !== null ? current : (operands[operands.length - 1] || '0');
}

function clearAll() {
    current = null;
    operator = null;
    operands = [];
    operators = [];
    renderDisplay();
}

function handleNumber(num) {
    if (current === null) {
        current = num.toString();
    } else {
        current += num.toString();
    }
    renderDisplay();
}

function handleOperator(op) {
    // Se não houver número atual e nenhum operando, permite começar com negativo
    if (current === null && operands.length === 0) {
        if (op === '-') {
            current = '-';
            renderDisplay();
        }
        return;
    }
    
    // Se houver um número atual, adiciona aos operandos
    if (current !== null) {
        // Se o último operando for igual ao número atual, não adiciona novamente
        if (operands.length === 0 || operands[operands.length - 1] !== parseFloat(current)) {
            operands.push(parseFloat(current));
        }
    }
    
    // Se já tivermos um operador e pelo menos 2 operandos, realiza o cálculo
    if (operator && operands.length >= 2) {
        const result = calculate(operands.slice(-2), operator);
        operands = [result];
        current = result.toString();
    }
    
    // Se não houver operando ainda, usa o último resultado (se existir)
    if (operands.length === 0 && current !== null) {
        operands.push(parseFloat(current));
    }
    
    // Atualiza o operador e limpa o número atual
    operator = op;
    current = null;
    
    renderDisplay();
}

function calculate(nums, op) {
    if (nums.length < 2) return nums[0] || 0;
    
    const a = parseFloat(nums[0]);
    const b = parseFloat(nums[1]);
    
    switch (op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': 
            if (b === 0) {
                alert('Erro: Divisão por zero!');
                return 0;
            }
            return a / b;
        default: return b;
    }
}

function handleEqual() {
    if (current === null || operator === null || operands.length === 0) {
        return;
    }
    
    // Adiciona o número atual aos operandos
    operands.push(parseFloat(current));
    
    // Realiza o cálculo final
    const result = calculate(operands.slice(-2), operator);
    
    // Formata a expressão para exibição
    const expression = `${operands[0]} ${operator} ${operands[1]}`;
    
    // Atualiza o display com o resultado
    current = result.toString();
    operator = null;
    operands = [result];
    operators = [];
    
    // Renderiza o display antes de adicionar ao histórico
    renderDisplay();
    
    // Limpa o display de expressão após um curto atraso para melhor UX
    setTimeout(() => {
        expressionDisplay.textContent = '\u00A0'; // Espaço em branco
    }, 0,1);
    
    // Adiciona ao histórico APENAS UMA VEZ
    addToHistory(expression, result);
    
    // Envia para o backend, se autenticado
    if (accessToken) {
        sendToBackend(expression, result);
    }
}

async function sendToBackend(expression, result) {
    try {
        // Extrai os operandos e o operador da expressão
        const parts = expression.split(' ');
        if (parts.length < 3) return; // Expressão inválida
        
        const num1 = parseFloat(parts[0]);
        const operator = parts[1];
        const num2 = parseFloat(parts[2]);
        
        // Mapeia os operadores para o formato esperado pelo backend
        const operatorMap = {
            '+': 'soma',
            '-': 'subtracao',
            '*': 'multiplicacao',
            '/': 'divisao',
            '%': 'modulo'
        };
        
        const tipoOperacao = operatorMap[operator];
        if (!tipoOperacao) return; // Operador não suportado
        
        // Prepara os dados para enviar ao backend
        const dados = {
            numeros: [num1, num2],
            tipo_operacao: tipoOperacao,
            resultado: result
        };
        
        console.log('Enviando cálculo para o backend:', dados);
        
        // Envia a requisição para o backend
        const response = await apiRequest(`${API_BASE}/calc/calcular/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(dados)
        });
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            console.error('Erro ao salvar cálculo no backend:', error);
            return;
        }
        
        console.log('Cálculo salvo com sucesso no backend');
        
        // Atualiza o histórico após salvar no backend
        await fetchHistory();
        
    } catch (error) {
        console.error('Erro ao enviar cálculo para o backend:', error);
    }
}

function addToHistory(expr, result) {
    // Adiciona ao histórico local
    history.unshift({
        expression: expr,
        result: result,
        timestamp: new Date().toISOString()
    });
    
    // Limita o histórico a 50 itens
    if (history.length > 50) {
        history.pop();
    }
    
    renderHistory();
}

function renderHistory() {
    if (!historyList) {
        console.error('Elemento historyList não encontrado');
        return;
    }
    
    historyList.innerHTML = '';
    
    if (!history || history.length === 0) {
        const emptyMsg = document.createElement('div');
        emptyMsg.className = 'history-empty';
        emptyMsg.textContent = 'Nenhuma operação recente';
        historyList.appendChild(emptyMsg);
        return;
    }
    
    history.slice(0, 10).forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'history-item';
        
        // Usa a propriedade correta (expr ou expression)
        const expression = item.expression || item.expr || '';
        const result = item.result || '';
        const itemId = item.id || item.pk;
        
        div.innerHTML = `
            <div class="history-content">
                <div class="history-expr">${expression}</div>
                <div class="history-result">= ${result}</div>
            </div>
            <button class="history-delete" title="Excluir">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    <line x1="10" y1="11" x2="10" y2="17"></line>
                    <line x1="14" y1="11" x2="14" y2="17"></line>
                </svg>
            </button>
        `;
        
        // Adiciona o evento de clique para o botão de exclusão
        const deleteBtn = div.querySelector('.history-delete');
        deleteBtn.onclick = (e) => deleteHistoryItem(index, itemId, e);
        
        div.onclick = () => {
            // Preenche a calculadora com o histórico selecionado
            if (item.expression && item.result) {
                // Formato novo (expression/result)
                const parts = item.expression.split(' ');
                if (parts.length >= 3) {
                    current = parts[2];
                    operator = parts[1];
                    operands = [parseFloat(parts[0])];
                    renderDisplay();
                }
            } else if (item.expr && item.result) {
                // Formato antigo (expr/result)
                const parts = item.expr.split(' ');
                if (parts.length >= 3) {
                    current = parts[2];
                    operator = parts[1];
                    operands = [parseFloat(parts[0])];
                    renderDisplay();
                }
            }
        };
        
        historyList.appendChild(div);
    });
}

// Função para excluir um item do histórico
async function deleteHistoryItem(index, itemId, event) {
    // Impede que o clique na lixeira dispare o evento de clique do item
    event.stopPropagation();
    
    if (!confirm('Tem certeza que deseja excluir este item do histórico?')) {
        return;
    }
    
    try {
        // Remove do histórico local
        history.splice(index, 1);
        
        // Se estiver autenticado, remove também do backend
        if (accessToken && itemId) {
            const response = await apiRequest(`${API_BASE}/calc/operacao/${itemId}/deletar/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                }
            });
            
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                console.error('Erro ao excluir item do histórico:', error);
                // Recarrega o histórico em caso de erro para manter a consistência
                await fetchHistory();
                return;
            }
        }
        
        // Atualiza a exibição
        renderHistory();
        
    } catch (error) {
        console.error('Erro ao excluir item do histórico:', error);
    }
}

function handleClear() {
    clearAll();
}
function handleInvert() {
    if (current !== null) {
        current = (parseFloat(current) * -1).toString();
        renderDisplay(current);
    }
}
function handlePercent() {
    if (current !== null) {
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
document.querySelector('.btn.multiply').onclick = () => handleOperator('*');
document.querySelector('.btn.divide').onclick = () => handleOperator('/');
document.querySelector('.btn.percent').onclick = () => handleOperator('%');
document.querySelector('.btn.equal').onclick = () => handleEqual();
document.querySelector('.btn.clear').onclick = () => handleClear();
document.querySelector('.btn.invert').onclick = () => handleInvert();
document.querySelector('.btn.dot').onclick = () => handleDot();

// Função para limpar o histórico local e no backend
async function clearHistory() {
    try {
        // Limpa o histórico local
        history = [];
        
        // Se estiver autenticado, limpa também no backend
        if (accessToken) {
            const response = await apiRequest(`${API_BASE}/calc/limpar_historico/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                }
            });
            
            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                console.error('Erro ao limpar histórico no backend:', error);
                // Mesmo com erro, continua para limpar o local
            } else {
                const result = await response.json();
                console.log(`Histórico limpo: ${result.count} operações removidas`);
            }
        }
        
        // Atualiza a exibição
        renderHistory();
        
    } catch (error) {
        console.error('Erro ao limpar histórico:', error);
    }
}

document.querySelector('.btn.clear-history').onclick = () => {
    if (confirm('Tem certeza que deseja apagar todo o histórico de operações?')) {
        clearHistory();
    }
};

window.onload = async () => {
    clearAll();
    loadTokens();
    if (!accessToken) {
        showLoginModal(true);
        setUserInfo(null);
        return;
    }
    // Tenta buscar perfil
    try {
        const resp = await apiRequest(`${API_BASE}/auth/perfil/`);
        if (resp.ok) {
            user = await resp.json();
            setUserInfo(user);
            showLoginModal(false);
            await fetchHistory();
        } else {
            logout();
        }
    } catch (e) {
        logout();
    }
};

// Alternar entre formulários de login e registro
function showRegisterForm(show = true) {
    loginForm.style.display = show ? 'none' : 'flex';
    registerForm.style.display = show ? 'flex' : 'none';
    loginError.style.display = 'none';
    registerError.textContent = '';
}

showRegisterLink.onclick = (e) => {
    e.preventDefault();
    showRegisterForm(true);
};

showLoginLink.onclick = (e) => {
    e.preventDefault();
    showRegisterForm(false);
};

loginForm.onsubmit = async (e) => {
    e.preventDefault();
    loginError.style.display = 'none';
    const email = loginEmail.value.trim();
    const senha = loginSenha.value;
    try {
        const resp = await fetch(`${API_BASE}/auth/login/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, senha})
        });
        const data = await resp.json();
        if (resp.ok && data.tokens) {
            saveTokens(data.tokens.access, data.tokens.refresh);
            user = data.user;
            setUserInfo(user);
            showLoginModal(false);
            loginForm.reset();
            await fetchHistory();
        } else {
            loginError.textContent = data.error || 'Falha ao fazer login.';
            loginError.style.display = 'block';
        }
    } catch (e) {
        loginError.textContent = 'Erro de conexão.';
        loginError.style.display = 'block';
    }
};

// Adicionar lógica de registro
registerForm.onsubmit = async (e) => {
    e.preventDefault();
    
    const nome = document.getElementById('register-nome').value.trim();
    const username = document.getElementById('register-username').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password1 = document.getElementById('register-password1').value;
    const password2 = document.getElementById('register-password2').value;
    
    registerError.textContent = '';
    
    // Validação básica
    if (password1 !== password2) {
        registerError.textContent = 'As senhas não conferem.';
        return;
    }
    
    if (password1.length < 8) {  
        registerError.textContent = 'A senha deve ter pelo menos 8 caracteres.';
        return;
    }
    
    try {
        const resp = await fetch(`${API_BASE}/auth/registro/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                nome,
                username,
                email,
                senha: password1,
                confirmar_senha: password2  
            })
        });
        
        const data = await resp.json();
        
        if (resp.ok && data.tokens) {
            // Registro bem-sucedido
            saveTokens(data.tokens.access, data.tokens.refresh);
            user = data.user;
            setUserInfo(user);
            showLoginModal(false);
            registerForm.reset();
            await fetchHistory();
            
            // Mostrar mensagem de sucesso
            alert('Conta criada com sucesso! Bem-vindo(a) ' + (user.nome || user.username) + '!');
        } else {
            // Mostrar erros de validação
            let errorMessage = 'Erro ao criar conta.';
            if (data.errors) {
                // Se o backend retornar erros específicos
                const errors = [];
                for (const [field, messages] of Object.entries(data.errors)) {
                    errors.push(`${field}: ${messages.join('. ')}`);
                }
                errorMessage = errors.join('\n');
            } else if (data.detail) {
                errorMessage = data.detail;
            } else if (data.error) {
                errorMessage = data.error;
            }
            registerError.textContent = errorMessage;
            registerError.style.display = 'block';
        }
    } catch (e) {
        console.error('Erro ao registrar:', e);
        registerError.textContent = 'Erro de conexão. Tente novamente mais tarde.';
        registerError.style.display = 'block';
    }
};

logoutBtn.onclick = async () => {
    try {
        // Chama a API para logout com o refresh token
        if (refreshToken) {
            const resp = await fetch(`${API_BASE}/auth/logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            });
            
            // Se a resposta for 401 (não autorizado), o token de acesso pode ter expirado
            // Mas ainda tentamos fazer o logout localmente
            if (!resp.ok && resp.status !== 401) {
                console.warn('Aviso: logout no servidor retornou status', resp.status);
                const data = await resp.json().catch(() => ({}));
                console.warn('Detalhes do erro:', data);
                
                // Se o erro for porque o refresh token é inválido, ainda assim fazemos logout local
                if (data.error && data.error.includes('refresh')) {
                    console.log('Refresh token inválido, fazendo logout local...');
                } else {
                    // Mostra mensagem de erro para o usuário (opcional)
                    alert('Ocorreu um erro ao fazer logout. Por favor, tente novamente.');
                }
            }
        }
    } catch (error) {
        console.error('Erro durante o logout:', error);
    } finally {
        // Sempre faz o logout local, independente da resposta da API
        logout();
    }
};

async function fetchHistory() {
    try {
        // Se não estiver autenticado, usa o histórico local
        if (!accessToken) {
            renderHistory();
            return;
        }
        
        const resp = await apiRequest(`${API_BASE}/calc/historico/`);
        if (resp.ok) {
            const data = await resp.json();
            // Converte o formato do histórico do backend para o formato esperado
            history = (data.results || data).map(item => ({
                id: item.id,  // Inclui o ID da operação
                expression: item.parametros_display,
                result: item.resultado_serializado,
                timestamp: item.data_criacao,
                // Mantém compatibilidade com formato antigo
                expr: item.parametros_display,
                pk: item.id
            }));
            
            // Ordena por data (mais recente primeiro)
            history.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
            
            console.log('Histórico carregado:', history);
            renderHistory();
        } else {
            // Se houver erro, usa o histórico local
            console.error('Erro ao carregar histórico:', await resp.text());
            renderHistory();
        }
    } catch (error) {
        console.error('Erro ao carregar histórico:', error);
        renderHistory();
    }
}
