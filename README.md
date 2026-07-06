# Asterix Consultoria Imobiliaria

Aplicacao web imobiliaria com experiencia inspirada na fluidez de imobiliárias, identidade propria da Asterix e arquitetura separada entre frontend Angular e backend FastAPI.

## Stack

- Frontend: Angular 21, TypeScript, Angular Router, Signals, RXJS, SCSS e Angular Material no painel administrativo.
- Backend: FastAPI, SQLAlchemy, PostgreSQL, Alembic, Pydantic, JWT, CORS e upload local.
- Imagens: salvas em `backend/uploads/imoveis/` e servidas por `/uploads/imoveis/{arquivo}`.

> Observacao: `@angular/cli@latest` resolveu para Angular 22 neste ambiente em 01/07/2026, mas exige Node 24.15+. Como o Node instalado e o Dockerfile estao em 24.13, o projeto foi criado em Angular 21, a major estavel compativel com este runtime.

## Como rodar com Docker

```bash
docker compose up --build
```

- Site: http://localhost:4200
- API: http://localhost:8001
- Swagger: http://localhost:8001/docs
- Admin: http://localhost:4200/admin/login

Credenciais iniciais:

- Email: `admin@asterix.com.br`
- Senha: `admin123`

## Como rodar localmente

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

Se a porta `8000` estiver ocupada pelo Docker Desktop no Windows, use:

```bash
uvicorn app.main:app --reload --port 8001
```

Frontend:

```bash
cd frontend
npm install
npm start
```

## Endpoints principais

- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/imoveis`
- `POST /api/imoveis`
- `GET /api/imoveis/{id}`
- `PATCH /api/imoveis/{id}`
- `DELETE /api/imoveis/{id}`
- `POST /api/imoveis/{id}/imagens`
- `PATCH /api/imoveis/{id}/imagens/{imagem_id}`
- `DELETE /api/imoveis/{id}/imagens/{imagem_id}`
- `GET /api/usuarios`
- `POST /api/usuarios`
- `POST /api/contato`
- `GET /api/dashboard`

## Estrutura

```text
backend/
  app/
    api/routes/
    core/
    db/
    models/
    schemas/
    services/
  alembic/
  uploads/imoveis/
frontend/
  src/app/
    admin/
    core/
    public/
    shared/
```

## Proximos passos naturais

- Integrar envio real do formulario de contato.
- Trocar o placeholder de WhatsApp pelo numero oficial.
- Adicionar metricas reais de acesso.
- Conectar Google Maps API com chave propria quando houver conta configurada.
