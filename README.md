# Kogui Calculadora

Uma calculadora web com autenticação de usuários, histórico de operações e API RESTful.

## 🚀 Começando

### Pré-requisitos

- Python 3.8+
- SQLite

### 🔧 Configuração do Ambiente

1. **Clonar o repositório**
   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd kogui
   ```

2. **Configurar ambiente virtual**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variáveis de ambiente**
   Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:
   ```env
    Deixado propositalmente para acessar o banco de dados
   ```

5. **Aplicar migrações**
   ```bash
   python manage.py migrate
   ```

6. **Criar superusuário (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

## 🖥️ Executando o Projeto

### Backend (Django)
```bash
python manage.py runserver
```

### Frontend
O frontend está disponível em:
- **URL Principal**: http://localhost:8000/static/calculadora/index.html
- **Admin**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/swagger/

## 📚 Documentação da API

### Autenticação
A API usa JWT (JSON Web Tokens) para autenticação. Inclua o token nas requisições:
```
Authorization: Bearer seu_token_aqui
```

### Endpoints Principais

#### Autenticação
- `POST /api/auth/registro/` - Registrar novo usuário
- `POST /api/auth/login/` - Fazer login
- `POST /api/auth/logout/` - Fazer logout
- `GET /api/auth/perfil/` - Ver perfil do usuário

#### Calculadora
- `POST /api/calc/calcular/` - Realizar cálculo
- `GET /api/calc/historico/` - Ver histórico de operações
- `GET /api/calc/operacao/{id}/` - Detalhes de uma operação
- `DELETE /api/calc/operacao/{id}/deletar/` - Excluir operação
- `POST /api/calc/limpar_historico/` - Limpar histórico

### Exemplo de Requisição
```http
POST /api/calc/calcular/
Content-Type: application/json
Authorization: Bearer seu_token

{
    "numeros": [10, 5, 2],
    "tipo_operacao": "soma"
}
```

## 🛠️ Desenvolvimento

### Estrutura do Projeto
```
kogui/
├── autenticacao/       # App de autenticação
├── calculadora/        # App da calculadora
├── kogui_portal/       # Configurações do projeto
├── static/             # Arquivos do frontend
└── templates/          # Templates HTML
```

### Comandos Úteis

```bash
- Criar migrações
python manage.py makemigrations

- Aplicar migrações
python manage.py migrate

- Criar superusuário
python manage.py createsuperuser

```

## 📦 Dependências Principais

### Backend
- Django 4.2
- Django REST Framework
- djangorestframework-simplejwt
- django-cors-headers
- python-dotenv
- drf-yasg (Documentação da API)


---

Desenvolvido para Kogui  por [Josué Alisson]
