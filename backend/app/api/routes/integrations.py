from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import verify_integration_token
from app.db.session import get_db
from app.models.imagem import Imagem
from app.models.imovel import Imovel
from app.schemas.imagem import ImagemRead
from app.schemas.imovel import ImovelCreate, ImovelRead
from app.services.files import save_upload

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


@router.post("/imoveis", response_model=ImovelRead, status_code=201)
def create_imovel(payload: ImovelCreate, db: Session = Depends(get_db)) -> Imovel:
    imovel = Imovel(**payload.model_dump())
    db.add(imovel)
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
    return [add_image_url(imagem) for imagem in imagens]
