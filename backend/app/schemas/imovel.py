from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.imagem import ImagemRead


TipoAnuncio = Literal["Aluguel", "Venda"]


class ImovelBase(BaseModel):
    nome: str = Field(min_length=3, max_length=180)
    descricao_curta: str | None = Field(default=None, min_length=10, max_length=300)
    descricao: str | None = Field(default=None, min_length=20)
    preco: Decimal | None = Field(default=None, gt=0)
    cidade: str | None = None
    bairro: str | None = None
    endereco: str | None = None
    tipo: str | None = None
    tipo_anuncio: TipoAnuncio | None = None
    numero: str | None = Field(default=None, max_length=30)
    area: int | None = Field(default=None, ge=1)
    quartos: int | None = Field(default=None, ge=0)
    banheiros: int | None = Field(default=None, ge=0)
    garagem: int | None = Field(default=None, ge=0)
    status: str = "Disponivel"
    destacado: bool = False


class ImovelCreate(ImovelBase):
    pass


class ImovelUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=180)
    descricao_curta: str | None = Field(default=None, min_length=10, max_length=300)
    descricao: str | None = Field(default=None, min_length=20)
    preco: Decimal | None = Field(default=None, gt=0)
    cidade: str | None = None
    bairro: str | None = None
    endereco: str | None = None
    tipo: str | None = None
    tipo_anuncio: TipoAnuncio | None = None
    numero: str | None = Field(default=None, max_length=30)
    area: int | None = Field(default=None, ge=1)
    quartos: int | None = Field(default=None, ge=0)
    banheiros: int | None = Field(default=None, ge=0)
    garagem: int | None = Field(default=None, ge=0)
    status: str | None = None
    destacado: bool | None = None


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
