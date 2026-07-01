from fastapi import APIRouter

from app.schemas.contato import ContatoCreate, ContatoRead

router = APIRouter(prefix="/contato", tags=["Contato"])


@router.post("", response_model=ContatoRead)
def send_contact(payload: ContatoCreate) -> ContatoRead:
    return ContatoRead(**payload.model_dump(), recebido=True)

