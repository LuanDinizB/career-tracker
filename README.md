# Career Tracker API
API simples para acompanhar empresas, vagas e candidaturas durante uma busca de emprego.
O projeto foi feito com FastAPI e MongoDB.
## O que dá para fazer
- Cadastrar, listar, buscar e remover empresas
- Cadastrar, listar, buscar e remover vagas
- Criar, listar, atualizar status e remover candidaturas
- Consultar um resumo das candidaturas por status
## Tecnologias
- Python
- FastAPI
- MongoDB
- PyMongo
- Uvicorn
## Como rodar
### 1. Clone o projeto

git clone git@github.com:LuanDinizB/career-tracker.git
cd career-tracker

Se você já está com a pasta aberta, só entre nela pelo terminal.
### 2. Crie o ambiente virtual

No PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

No macOS ou Linux:

python -m venv .venv
source .venv/bin/activate

### 3. Instale as dependências

pip install -r requirements.txt

### 4. Configure o `.env`
Crie um arquivo chamado `.env` na raiz do projeto:
env
MONGO_URI=mongodb://localhost:27017/career_tracker

Também funciona com MongoDB Atlas, desde que a URL tenha o nome do banco no final:
env
MONGO_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/career_tracker

### 5. Suba a API

fastapi dev app/main.py

## Rotas principais
### Empresas
text
POST   /companies
GET    /companies
GET    /companies/{company_id}
DELETE /companies/{company_id}

### Vagas
text
POST   /jobs
GET    /jobs
GET    /jobs/{job_id}
DELETE /jobs/{job_id}

### Candidaturas
text
POST   /applications
GET    /applications
PATCH  /applications/{application_id}/status
DELETE /applications/{application_id}

A listagem de candidaturas aceita filtros por query string:
text
GET /applications?status=applied
GET /applications?candidate_email=email@exemplo.com


### Métricas
text
GET /metrics/summary

## Estrutura
text
app/
  main.py
  database.py
  schemas.py
  routes/
    applications.py
    companies.py
    jobs.py
    metrics.py
requirements.txt
