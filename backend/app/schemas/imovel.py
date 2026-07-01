from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.imagem import ImagemRead


class ImovelBase(BaseModel):
    nome: str = Field(min_length=3, max_length=180)
    descricao_curta: str = Field(min_length=10, max_length=300)
    descricao: str = Field(min_length=20)
    preco: Decimal = Field(gt=0)
    cidade: str
    bairro: str
    endereco: str
    tipo: str
    area: int = Field(ge=1)
    quartos: int = Field(ge=0)
    banheiros: int = Field(ge=0)
    garagem: int = Field(ge=0)
    status: str = "Disponivel"


class ImovelCreate(ImovelBase):
    pass


class ImovelUpdate(BaseModel):
    nome: str | None = None
    descricao_curta: str | None = None
    descricao: str | None = None
    preco: Decimal | None = Field(default=None, gt=0)
    cidade: str | None = None
    bairro: str | None = None
    endereco: str | None = None
    tipo: str | None = None
    area: int | None = Field(default=None, ge=1)
    quartos: int | None = Field(default=None, ge=0)
    banheiros: int | None = Field(default=None, ge=0)
    garagem: int | None = Field(default=None, ge=0)
    status: str | None = None


class ImovelRead(ImovelBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    imagens: list[ImagemRead] = []


class ImovelList(BaseModel):
    items: list[ImovelRead]
    total: int
    page: int
    size: int

