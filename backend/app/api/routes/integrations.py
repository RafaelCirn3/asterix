from decimal import Decimal

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.api.deps import verify_integration_token
from app.db.session import get_db
from app.models.imagem import Imagem
from app.models.imovel import Imovel
from app.schemas.imagem import ImagemRead
from app.schemas.imovel import ImovelCreate, ImovelList, ImovelRead, ImovelUpdate
from app.services.files import MAX_IMAGES_PER_PROPERTY, delete_upload, save_upload

router = APIRouter(
    prefix="/integrations",
    tags=["Integracoes"],
    dependencies=[Depends(verify_integration_token)],
)


def with_image_urls(imovel: Imovel) -> Imovel:
    for imagem in imovel.imagens:
        imagem.url = f"/uploads/imoveis/{imagem.arquivo}"
    return imovel


def add_image_url(imagem: Imagem) -> Imagem:
    imagem.url = f"/uploads/imoveis/{imagem.arquivo}"
    return imagem


@router.get("/imoveis", response_model=ImovelList)
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
    size: int = Query(default=20, ge=1, le=100),
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
    items = db.scalars(stmt.offset((page - 1) * size).limit(size)).all()
    return ImovelList(items=[with_image_urls(item) for item in items], total=total, page=page, size=size)


@router.get("/imoveis/{imovel_id}", response_model=ImovelRead)
def get_imovel(imovel_id: int, db: Session = Depends(get_db)) -> Imovel:
    imovel = db.scalar(
        select(Imovel).options(selectinload(Imovel.imagens)).where(Imovel.id == imovel_id)
    )
    if imovel is None:
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")
    return with_image_urls(imovel)


@router.post("/imoveis", response_model=ImovelRead, status_code=201)
def create_imovel(payload: ImovelCreate, db: Session = Depends(get_db)) -> Imovel:
    imovel = Imovel(**payload.model_dump())
    db.add(imovel)
    db.commit()
    db.refresh(imovel)
    return with_image_urls(imovel)


@router.patch("/imoveis/{imovel_id}", response_model=ImovelRead)
def update_imovel(
    imovel_id: int,
    payload: ImovelUpdate,
    db: Session = Depends(get_db),
) -> Imovel:
    imovel = db.get(Imovel, imovel_id)
    if imovel is None:
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(imovel, field, value)

    db.commit()
    db.refresh(imovel)
    return with_image_urls(imovel)


@router.post("/imoveis/{imovel_id}/imagens", response_model=list[ImagemRead], status_code=201)
async def upload_imagens(
    imovel_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
) -> list[Imagem]:
    if db.get(Imovel, imovel_id) is None:
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")
    if not files:
        raise HTTPException(status_code=400, detail="Nenhuma imagem foi enviada")

    current_count = db.scalar(
        select(func.count(Imagem.id)).where(Imagem.imovel_id == imovel_id)
    ) or 0
    if current_count + len(files) > MAX_IMAGES_PER_PROPERTY:
        available = max(0, MAX_IMAGES_PER_PROPERTY - current_count)
        raise HTTPException(
            status_code=400,
            detail=(
                f"Cada imovel pode ter no maximo {MAX_IMAGES_PER_PROPERTY} imagens. "
                f"Este imovel ainda permite {available}."
            ),
        )

    imagens: list[Imagem] = []
    saved_files: list[str] = []
    try:
        for index, file in enumerate(files):
            arquivo = await save_upload(file)
            saved_files.append(arquivo)
            imagem = Imagem(
                imovel_id=imovel_id,
                arquivo=arquivo,
                principal=current_count == 0 and index == 0,
                ordem=current_count + index,
            )
            db.add(imagem)
            imagens.append(imagem)
        db.commit()
    except ValueError as exc:
        db.rollback()
        for filename in saved_files:
            delete_upload(filename)
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception:
        db.rollback()
        for filename in saved_files:
            delete_upload(filename)
        raise

    for imagem in imagens:
        db.refresh(imagem)
    return [add_image_url(imagem) for imagem in imagens]
