# Asterix MCP

Servidor MCP do Asterix para operacoes controladas sobre o catalogo de imoveis.

## Escopo inicial

O servidor expoe somente quatro ferramentas:

- `listar_imoveis`: lista e filtra imoveis;
- `ver_imovel`: consulta um imovel pelo ID;
- `criar_imovel`: cadastra um novo imovel;
- `editar_imovel`: altera campos de um imovel existente.

Nao existem ferramentas de exclusao, usuarios ou administracao do banco nesta versao.

## Arquitetura

```text
Cliente MCP
    |
    | Streamable HTTP
    v
Asterix MCP
    |
    | HTTP + INTEGRATION_TOKEN
    v
FastAPI (backend:8000/api)
    |
    v
PostgreSQL
```

O MCP nunca acessa o PostgreSQL diretamente. Toda operacao passa pela API de integracao do backend.

## Variaveis

O servico utiliza:

```env
INTEGRATION_TOKEN=<mesmo token configurado no backend>
ASTERIX_API_URL=http://backend:8000/api
```

Em producao, `ASTERIX_API_URL` ja e definido pelo `docker-compose.prod.yml`. O token deve existir apenas no ambiente e nunca ser commitado.

## Execucao em producao

```bash
docker compose -f docker-compose.prod.yml build mcp backend
docker compose -f docker-compose.prod.yml up -d backend mcp
docker compose -f docker-compose.prod.yml logs -f mcp
```

O container MCP fica disponivel apenas no loopback da VPS em `127.0.0.1:8002`, e o endpoint MCP e `/mcp`.

Para testar da propria VPS:

```text
http://127.0.0.1:8002/mcp
```

Antes de conectar um cliente MCP externo, deve ser adicionada uma camada de autenticacao na entrada publica e configurado o proxy HTTPS. Nao exponha a porta 8002 diretamente para a internet.

## Semantica de campos opcionais

- `null`: informacao nao fornecida/desconhecida;
- `0`: valor conhecido como zero. Exemplo: `garagem = 0` significa que o imovel nao possui vaga;
- valores positivos: quantidade ou valor conhecido.
