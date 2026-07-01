from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.imovel import Imovel

router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_user)])


@router.get("")
def dashboard(db: Session = Depends(get_db)) -> dict:
    total = db.scalar(select(func.count(Imovel.id))) or 0
    ultimos = db.scalars(select(Imovel).order_by(Imovel.created_at.desc()).limit(5)).all()
    return {
        "quantidade_imoveis": total,
        "quantidade_acessos": 0,
        "ultimos_imoveis": [
            {"id": item.id, "nome": item.nome, "cidade": item.cidade, "preco": float(item.preco)} for item in ultimos
        ],
    }

