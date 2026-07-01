from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.auth import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["Autenticacao"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    usuario = db.scalar(select(Usuario).where(Usuario.email == payload.email))
    if usuario is None or not verify_password(payload.senha, usuario.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais invalidas")
    return Token(access_token=create_access_token(usuario.id), usuario=usuario)


@router.post("/logout")
def logout() -> dict[str, bool]:
    return {"ok": True}

