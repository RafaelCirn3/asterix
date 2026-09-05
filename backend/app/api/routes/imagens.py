from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import require_editor
from app.db.session import get_db
from app.models.imagem import Imagem
from app.models.imovel import Imovel
from app.models.usuario import Usuario
from app.schemas.imagem import ImagemRead, ImagemUpdate
from app.services.files import MAX_IMAGES_PER_PROPERTY, delete_upload, save_upload

router = APIRouter(prefix="/imoveis/{imovel_id}/imagens", tags=["Imagens"], dependencies=[Depends(require_editor)])


def add_url(imagem: Imagem) -> Imagem:
    imagem.url = f"/uploads/imoveis/{imagem.arquivo}"
    return imagem


def normalize_images(db: Session, imovel_id: int) -> None:
    imagens = list(
        db.scalars(
            select(Imagem).where(Imagem.imovel_id == imovel_id).order_by(Imagem.ordem, Imagem.id)
        ).all()
    )
    for index, item in enumerate(imagens):
        item.ordem = index
    if imagens and not any(item.principal for item in imagens):
        imagens[0].principal = True


@router.post("", response_model=list[ImagemRead])
async def upload_imagens(
    imovel_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_editor),
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
    return [add_url(imagem) for imagem in imagens]


@router.patch("/{imagem_id}", response_model=ImagemRead)
def update_imagem(
    imovel_id: int,
    imagem_id: int,
    payload: ImagemUpdate,
    db: Session = Depends(get_db),
) -> Imagem:
    imagem = db.get(Imagem, imagem_id)
    if imagem is None or imagem.imovel_id != imovel_id:
        raise HTTPException(status_code=404, detail="Imagem nao encontrada")
    if payload.principal:
        for item in db.scalars(select(Imagem).where(Imagem.imovel_id == imovel_id)).all():
            item.principal = False
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(imagem, field, value)
    normalize_images(db, imovel_id)
    db.commit()
    db.refresh(imagem)
    return add_url(imagem)


@router.delete("/{imagem_id}", status_code=204)
def delete_imagem(imovel_id: int, imagem_id: int, db: Session = Depends(get_db)) -> None:
    imagem = db.get(Imagem, imagem_id)
    if imagem is None or imagem.imovel_id != imovel_id:
        raise HTTPException(status_code=404, detail="Imagem nao encontrada")

    arquivo = imagem.arquivo
    db.delete(imagem)
    db.flush()
    normalize_images(db, imovel_id)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    delete_upload(arquivo)
