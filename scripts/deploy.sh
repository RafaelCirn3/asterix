#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/docker-compose.prod.yml"
ENV_FILE="$ROOT_DIR/.env.production"

cd "$ROOT_DIR"

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Working tree has local changes. Commit or stash them before deploying." >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing production env file: $ENV_FILE" >&2
  exit 1
fi

git pull --ff-only

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" config >/dev/null
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" build
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d --remove-orphans

backend_container_id="$(docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps -q backend)"
if [[ -z "$backend_container_id" ]]; then
  echo "Backend container was not created." >&2
  exit 1
fi

for _ in {1..60}; do
  health_status="$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$backend_container_id")"
  if [[ "$health_status" == "healthy" ]]; then
    break
  fi
  if [[ "$health_status" == "unhealthy" ]]; then
    echo "Backend container reported unhealthy." >&2
    docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" logs --no-color backend >&2
    exit 1
  fi
  sleep 2
done

if [[ "$(docker inspect --format='{{if .State.Health}}{{.State.Health.Status}}{{else}}none{{end}}' "$backend_container_id")" != "healthy" ]]; then
  echo "Backend did not become healthy in time." >&2
  docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" logs --no-color backend >&2
  exit 1
fi

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" exec -T backend alembic upgrade head
docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" ps
