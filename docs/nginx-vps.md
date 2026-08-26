# Nginx da VPS

Este projeto não altera `/etc/nginx` diretamente. Abaixo está a configuração esperada no host da VPS para publicar o frontend, encaminhar a API/uploads e, opcionalmente, publicar o MCP por HTTPS.

## Redirecionamento do `www`

```nginx
server {
  listen 80;
  server_name www.asterixconsultoria.com.br;
  return 301 https://asterixconsultoria.com.br$request_uri;
}

server {
  listen 443 ssl http2;
  server_name www.asterixconsultoria.com.br;
  ssl_certificate /etc/ssl/cloudflare/origin.crt;
  ssl_certificate_key /etc/ssl/cloudflare/origin.key;
  return 301 https://asterixconsultoria.com.br$request_uri;
}
```

## Domínio principal

```nginx
server {
  listen 80;
  server_name asterixconsultoria.com.br;
  return 301 https://asterixconsultoria.com.br$request_uri;
}

server {
  listen 443 ssl http2;
  server_name asterixconsultoria.com.br;

  ssl_certificate /etc/ssl/cloudflare/origin.crt;
  ssl_certificate_key /etc/ssl/cloudflare/origin.key;

  location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /api/ {
    proxy_pass http://127.0.0.1:8001;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }

  location /uploads/ {
    proxy_pass http://127.0.0.1:8001;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

## Subdomínio MCP

Crie um registro DNS `mcp` apontando para a mesma VPS. O certificado Cloudflare Origin usado neste bloco precisa cobrir `mcp.asterixconsultoria.com.br` (ou usar um wildcard compatível).

```nginx
server {
  listen 80;
  server_name mcp.asterixconsultoria.com.br;
  return 301 https://mcp.asterixconsultoria.com.br$request_uri;
}

server {
  listen 443 ssl http2;
  server_name mcp.asterixconsultoria.com.br;

  ssl_certificate /etc/ssl/cloudflare/origin.crt;
  ssl_certificate_key /etc/ssl/cloudflare/origin.key;

  location /mcp {
    proxy_pass http://127.0.0.1:8002;
    proxy_http_version 1.1;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # Preserva a credencial Bearer enviada pelo cliente MCP.
    proxy_set_header Authorization $http_authorization;

    # Necessario para respostas longas/streaming do transporte Streamable HTTP.
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 3600s;
    proxy_send_timeout 3600s;
  }

  location / {
    return 404;
  }
}
```

O endpoint externo fica:

```text
https://mcp.asterixconsultoria.com.br/mcp
```

O cliente MCP deve enviar `Authorization: Bearer <MCP_ACCESS_TOKEN>`. O `INTEGRATION_TOKEN` nunca deve sair da rede interna Docker.

Depois de alterar a configuração do host:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Observações

- O frontend escuta apenas em `127.0.0.1:8080`.
- O backend escuta apenas em `127.0.0.1:8001`.
- O MCP escuta no host apenas em `127.0.0.1:8002`.
- O PostgreSQL não recebe porta publicada.
- Não abra a porta `8002` no firewall/security group; o acesso externo deve passar somente pelo Nginx em HTTPS.
- O container do backend continua servindo uploads em `/uploads/imoveis/...`.
- Se você quiser expor documentação da API, use `https://asterixconsultoria.com.br/api/docs`.
