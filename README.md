# Asterix Consultoria Imobiliaria

Aplicacao web imobiliaria com frontend Angular, backend FastAPI, PostgreSQL e deploy via Docker Compose.

## Stack

- Frontend: Angular 21, TypeScript e SCSS.
- Backend: FastAPI, SQLAlchemy, PostgreSQL, Alembic, JWT e upload local.
- Banco: PostgreSQL em container.
- Deploy: Docker Compose com separacao entre desenvolvimento e producao.

## Desenvolvimento

Crie o arquivo de ambiente local a partir do exemplo:

```bash
cp backend/.env.example backend/.env
```

Suba a stack de desenvolvimento:

```bash
docker compose up --build
```

Endpoints locais:

- Frontend: `http://localhost:4200`
- API: `http://localhost:8001/api`
- Swagger: `http://localhost:8001/api/docs`
- Admin: `http://localhost:4200/admin/login`

## Produção

Crie o arquivo de ambiente de producao a partir do exemplo:

```bash
cp .env.production.example .env.production
```

Preencha os secrets antes de subir a stack.

Fluxo recomendado:

```bash
docker compose -f docker-compose.prod.yml config
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

Comandos uteis:

```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f frontend
docker compose -f docker-compose.prod.yml logs -f db
```

## Nginx Da VPS

Veja a configuracao sugerida em [`docs/nginx-vps.md`](/docs/nginx-vps.md).

Arquitetura esperada:

- `https://asterixconsultoria.com.br/` -> frontend em `127.0.0.1:8080`
- `https://asterixconsultoria.com.br/api/` -> backend em `127.0.0.1:8001`
- `https://asterixconsultoria.com.br/uploads/` -> backend em `127.0.0.1:8001`

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
docs/
```

## Observacoes

- O PostgreSQL nao publica porta no Compose de producao.
- O backend em producao fica preso a `127.0.0.1:8001`.
- O frontend em producao fica preso a `127.0.0.1:8080`.
- Uploads persistem em volume nomeado fora da camada efemera do container.
- `backend/.env` e `backend/asterix_local.db` nao devem ser versionados.
