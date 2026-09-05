from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import require_editor
from app.db.session import get_db
from app.models.usuario import Usuario
from app.schemas.imovel import ImovelCreate, ImovelList, ImovelRead, ImovelUpdate
from app.services import imoveis as imovel_service

router = APIRouter(prefix="/imoveis", tags=["Imoveis"])


@router.get("", response_model=ImovelList)
def list_imoveis(
    db: Session = Depends(get_db),
    cidade: str | None = None,
    bairro: str | None = None,
    tipo: str | None = None,
    destacado: bool | None = None,
    preco_min: Decimal | None = None,
    preco_max: Decimal | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=9, ge=1, le=100),
) -> ImovelList:
    items, total = imovel_service.list_imoveis(
        db,
        cidade=cidade,
        bairro=bairro,
        tipo=tipo,
        destacado=destacado,
        preco_min=preco_min,
        preco_max=preco_max,
        search=search,
        page=page,
        size=size,
    )
    return ImovelList(items=items, total=total, page=page, size=size)


@router.post("", response_model=ImovelRead)
def create_imovel(
    payload: ImovelCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_editor),
):
    return imovel_service.create_imovel(db, payload)


@router.get("/{imovel_id}", response_model=ImovelRead)
def get_imovel(imovel_id: int, db: Session = Depends(get_db)):
    imovel = imovel_service.get_imovel(db, imovel_id)
    if imovel is None:
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")
    return imovel


@router.patch("/{imovel_id}", response_model=ImovelRead)
def update_imovel(
    imovel_id: int,
    payload: ImovelUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_editor),
):
    imovel = imovel_service.update_imovel(db, imovel_id, payload)
    if imovel is None:
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")
    return imovel


@router.delete("/{imovel_id}", status_code=204)
def delete_imovel(
    imovel_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_editor),
) -> None:
    if not imovel_service.delete_imovel(db, imovel_id):
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")
