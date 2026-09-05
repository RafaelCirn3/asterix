from datetime import datetime, timezone
from secrets import compare_digest

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_access_token_payload
from app.db.session import get_db
from app.models.token_revogado import TokenRevogado
from app.models.usuario import Usuario

bearer_scheme = HTTPBearer()
integration_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    payload = decode_access_token_payload(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")

    subject = payload.get("sub")
    jti = payload.get("jti")
    if not subject or not jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")

    db.execute(delete(TokenRevogado).where(TokenRevogado.expires_at < datetime.now(timezone.utc)))
    if db.get(TokenRevogado, jti) is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revogado")

    try:
        user_id = int(subject)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido") from exc

    user = db.get(Usuario, user_id)
    if user is None or not user.ativo:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inativo ou inexistente")
    return user


def require_admin(user: Usuario = Depends(get_current_user)) -> Usuario:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissao de administrador necessaria")
    return user


def require_editor(user: Usuario = Depends(get_current_user)) -> Usuario:
    if user.role not in {"admin", "editor"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissao de edicao necessaria")
    return user


def verify_integration_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(integration_bearer_scheme),
) -> None:
    if not settings.integration_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Integracao externa nao configurada",
        )
    if (
        credentials is None
        or credentials.scheme.lower() != "bearer"
        or not compare_digest(credentials.credentials, settings.integration_token)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de integracao invalido",
        )
