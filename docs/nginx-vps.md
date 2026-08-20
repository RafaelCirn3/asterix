# Nginx da VPS

Este projeto não altera `/etc/nginx` diretamente. Abaixo está a configuração esperada no host da VPS para publicar o frontend e encaminhar a API e uploads para os containers locais.

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

## Observações

- O frontend escuta apenas em `127.0.0.1:8080`.
- O backend escuta apenas em `127.0.0.1:8001`.
- O PostgreSQL não recebe porta publicada.
- O container do backend continua servindo uploads em `/uploads/imoveis/...`.
- Se você quiser expor documentação da API, use `https://asterixconsultoria.com.br/api/docs`.
