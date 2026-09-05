from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.imovel import Imovel
from app.schemas.imovel import ImovelCreate, ImovelUpdate


def with_image_urls(imovel: Imovel) -> Imovel:
    for imagem in imovel.imagens:
        imagem.url = f"/uploads/imoveis/{imagem.arquivo}"
    return imovel


def list_imoveis(
    db: Session,
    *,
    cidade: str | None = None,
    bairro: str | None = None,
    tipo: str | None = None,
    destacado: bool | None = None,
    preco_min: Decimal | None = None,
    preco_max: Decimal | None = None,
    search: str | None = None,
    page: int = 1,
    size: int = 9,
) -> tuple[list[Imovel], int]:
    stmt = select(Imovel).options(selectinload(Imovel.imagens)).order_by(Imovel.created_at.desc())
    count_stmt = select(func.count(Imovel.id))
    filters = []
    if cidade:
        filters.append(Imovel.cidade.ilike(f"%{cidade}%"))
    if bairro:
        filters.append(Imovel.bairro.ilike(f"%{bairro}%"))
    if tipo:
        filters.append(Imovel.tipo == tipo)
    if destacado is not None:
        filters.append(Imovel.destacado.is_(destacado))
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
    items = list(db.scalars(stmt.offset((page - 1) * size).limit(size)).all())
    return [with_image_urls(item) for item in items], total


def get_imovel(db: Session, imovel_id: int) -> Imovel | None:
    imovel = db.scalar(select(Imovel).options(selectinload(Imovel.imagens)).where(Imovel.id == imovel_id))
    return with_image_urls(imovel) if imovel else None


def create_imovel(db: Session, payload: ImovelCreate) -> Imovel:
    imovel = Imovel(**payload.model_dump())
    db.add(imovel)
    db.commit()
    db.refresh(imovel)
    return with_image_urls(imovel)


def update_imovel(db: Session, imovel_id: int, payload: ImovelUpdate) -> Imovel | None:
    imovel = db.get(Imovel, imovel_id)
    if imovel is None:
        return None
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(imovel, field, value)
    db.commit()
    db.refresh(imovel)
    return with_image_urls(imovel)


def delete_imovel(db: Session, imovel_id: int) -> bool:
    imovel = db.get(Imovel, imovel_id)
    if imovel is None:
        return False
    db.delete(imovel)
    db.commit()
    return True
