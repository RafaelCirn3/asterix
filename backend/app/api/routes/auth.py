from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token_payload, verify_password
from app.db.session import get_db
from app.models.token_revogado import TokenRevogado
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["Autenticacao"])
bearer_scheme = HTTPBearer()


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    usuario = db.scalar(select(Usuario).where(Usuario.email == payload.email))
    if usuario is None or not usuario.ativo or not verify_password(payload.senha, usuario.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais invalidas")
    return Token(access_token=create_access_token(usuario.id), usuario=usuario)


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> dict[str, bool]:
    payload = decode_access_token_payload(credentials.credentials)
    if payload is None or not payload.get("jti") or not payload.get("exp"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")

    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    if expires_at > datetime.now(timezone.utc):
        db.merge(TokenRevogado(jti=payload["jti"], expires_at=expires_at))
        db.commit()
    return {"ok": True}
