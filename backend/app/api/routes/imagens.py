from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.imagem import Imagem
from app.models.imovel import Imovel
from app.models.usuario import Usuario
from app.schemas.imagem import ImagemRead, ImagemUpdate
from app.services.files import delete_upload, save_upload

router = APIRouter(prefix="/imoveis/{imovel_id}/imagens", tags=["Imagens"], dependencies=[Depends(get_current_user)])


def add_url(imagem: Imagem) -> Imagem:
    imagem.url = f"/uploads/imoveis/{imagem.arquivo}"
    return imagem


@router.post("", response_model=list[ImagemRead])
async def upload_imagens(
    imovel_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
) -> list[Imagem]:
    if db.get(Imovel, imovel_id) is None:
        raise HTTPException(status_code=404, detail="Imovel nao encontrado")
    current_count = len(db.scalars(select(Imagem).where(Imagem.imovel_id == imovel_id)).all())
    imagens: list[Imagem] = []
    for index, file in enumerate(files):
        try:
            arquivo = await save_upload(file)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        imagem = Imagem(
            imovel_id=imovel_id,
            arquivo=arquivo,
            principal=current_count == 0 and index == 0,
            ordem=current_count + index,
        )
        db.add(imagem)
        imagens.append(imagem)
    db.commit()
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
    db.commit()
    db.refresh(imagem)
    return add_url(imagem)


@router.delete("/{imagem_id}", status_code=204)
def delete_imagem(imovel_id: int, imagem_id: int, db: Session = Depends(get_db)) -> None:
    imagem = db.get(Imagem, imagem_id)
    if imagem is None or imagem.imovel_id != imovel_id:
        raise HTTPException(status_code=404, detail="Imagem nao encontrada")
    delete_upload(imagem.arquivo)
    db.delete(imagem)
    db.commit()

