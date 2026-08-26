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
    | HTTPS + Bearer MCP_ACCESS_TOKEN
    v
Nginx / Cloudflare
    |
    v
Asterix MCP (127.0.0.1:8002)
    |
    | HTTP interno + INTEGRATION_TOKEN
    v
FastAPI (backend:8000/api)
    |
    v
PostgreSQL
```

O MCP nunca acessa o PostgreSQL diretamente. Toda operacao passa pela API de integracao do backend.

## Separacao das credenciais

Existem duas credenciais diferentes e elas nao devem ser reutilizadas:

```env
# MCP -> backend
INTEGRATION_TOKEN=<token-interno>

# cliente externo -> MCP
MCP_ACCESS_TOKEN=<token-externo>
```

`INTEGRATION_TOKEN` autentica somente o container MCP contra `/api/integrations` do FastAPI. `MCP_ACCESS_TOKEN` protege o endpoint MCP publicado externamente e deve ser fornecido somente ao cliente MCP autorizado.

O cliente envia:

```http
Authorization: Bearer <MCP_ACCESS_TOKEN>
```

O token e comparado no servidor MCP antes de qualquer chamada de ferramenta. Uma credencial invalida recebe HTTP 401.

## Outras variaveis

```env
ASTERIX_API_URL=http://backend:8000/api
```

Em producao, `ASTERIX_API_URL` ja e definido pelo `docker-compose.prod.yml`. Secrets devem existir apenas no ambiente e nunca ser commitados.

## Execucao em producao

```bash
docker compose -f docker-compose.prod.yml build backend mcp
docker compose -f docker-compose.prod.yml up -d backend mcp
docker compose -f docker-compose.prod.yml logs -f mcp
```

O container MCP permanece publicado apenas no loopback da VPS em `127.0.0.1:8002`. A porta 8002 nunca deve ser aberta diretamente no firewall/security group.

O endpoint local e:

```text
http://127.0.0.1:8002/mcp
```

Depois do proxy HTTPS, o endpoint externo previsto e:

```text
https://mcp.asterixconsultoria.com.br/mcp
```

A configuracao de Nginx necessaria esta documentada em `docs/nginx-vps.md`.

## Semantica de campos opcionais

- `null`: informacao nao fornecida/desconhecida;
- `0`: valor conhecido como zero. Exemplo: `garagem = 0` significa que o imovel nao possui vaga;
- valores positivos: quantidade ou valor conhecido.
