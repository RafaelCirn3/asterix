from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.core.security import get_password_hash
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"], dependencies=[Depends(require_admin)])


@router.get("", response_model=list[UsuarioRead])
def list_usuarios(db: Session = Depends(get_db)) -> list[Usuario]:
    return list(db.scalars(select(Usuario).order_by(Usuario.nome)).all())


@router.post("", response_model=UsuarioRead)
def create_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)) -> Usuario:
    if db.scalar(select(Usuario).where(Usuario.email == payload.email)):
        raise HTTPException(status_code=409, detail="Email ja cadastrado")
    usuario = Usuario(
        nome=payload.nome,
        email=payload.email,
        senha_hash=get_password_hash(payload.senha),
        ativo=payload.ativo,
        role=payload.role,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioRead)
def update_usuario(usuario_id: int, payload: UsuarioUpdate, db: Session = Depends(get_db)) -> Usuario:
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    data = payload.model_dump(exclude_unset=True)
    if "email" in data:
        duplicate = db.scalar(select(Usuario).where(Usuario.email == data["email"], Usuario.id != usuario_id))
        if duplicate:
            raise HTTPException(status_code=409, detail="Email ja cadastrado")
    if "senha" in data:
        usuario.senha_hash = get_password_hash(data.pop("senha"))
    for field, value in data.items():
        setattr(usuario, field, value)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}", status_code=204)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)) -> None:
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if usuario.role == "admin":
        admin_count = db.scalar(select(Usuario).where(Usuario.role == "admin", Usuario.ativo.is_(True)).count())
        if admin_count == 1 and usuario.ativo:
            raise HTTPException(status_code=409, detail="Nao e permitido remover o ultimo administrador ativo")
    db.delete(usuario)
    db.commit()
