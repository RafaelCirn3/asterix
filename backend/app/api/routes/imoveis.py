from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.imovel import Imovel
from app.models.usuario import Usuario
from app.schemas.imovel import ImovelCreate, ImovelList, ImovelRead, ImovelUpdate

router = APIRouter(prefix="/imoveis", tags=["Imoveis"])


def with_image_urls(imovel: Imovel) -> Imovel:
    for imagem in imovel.imagens:
        imagem.url = f"/uploads/imoveis/{imagem.arquivo}"
    return imovel


@router.get("", response_model=ImovelList)
def list_imoveis(
    db: Session = Depends(get_db),
    cidade: str | None = None,
    bairro: str | None = None,
    tipo: str | None = None,
    preco_min: Decimal | None = None,
    preco_max: Decimal | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=9, ge=1, le=100),
) -> ImovelList:
    stmt = select(Imovel).options(selectinload(Imovel.imagens)).order_by(Imovel.created_at.desc())
    count_stmt = select(func.count(Imovel.id))
    filters = []
    if cidade:
        filters.append(Imovel.cidade.ilike(f"%{cidade}%"))
    if bairro:
        filters.append(Imovel.bairro.ilike(f"%{bairro}%"))
    if tipo:
        filters.append(Imovel.tipo == tipo)
    if preco_min is not None:
        filters.append(Imovel.preco >= preco_min)
    if preco_max is not None:
        filters.append(Imovel.preco <= preco_max)
    if search:
        filters.append(Imovel.nome.ilike(f"%{search}%"))
    if filters:
        stmt = stmt.where(*filters)
        count_stmt = count_stmt.where(*filters)
    total = db.scalar(count_stmt) or 0
    items = db.scalars(stmt.offset((page - 1) * size).limit(size)).all()
    return ImovelList(items=[with_image_urls(item) for item in items], total=total, page=page, size=size)


@router.post("", response_model=ImovelRead, dependencies=[Depends(get_current_user)])
def create_imovel(payload: ImovelCreate, db: Session = Depends(get_db)) -> Imovel:
    imovel = Imovel(**payload.model_dump())
    db.add(imovel)
    db.commit()
    db.refresh(imovel)
    return with_image_urls(imovel)


@router.get("/{imovel_id}", response_model=ImovelRead)
def get_imovel(imovel_id: int, db: Session = Depends(get_db)) -> Imovel:
    imovel = db.scalar(select(Imovel).options(selectinload(Imovel.imagens)).where(Imovel.id == imovel_id))
    if imovel is None:
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")
    return with_image_urls(imovel)


@router.patch("/{imovel_id}", response_model=ImovelRead)
def update_imovel(
    imovel_id: int,
    payload: ImovelUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> Imovel:
    imovel = db.get(Imovel, imovel_id)
    if imovel is None:
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(imovel, field, value)
    db.commit()
    db.refresh(imovel)
    return with_image_urls(imovel)


@router.delete("/{imovel_id}", status_code=204)
def delete_imovel(
    imovel_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> None:
    imovel = db.get(Imovel, imovel_id)
    if imovel is None:
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")
    db.delete(imovel)
    db.commit()

