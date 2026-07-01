from pydantic import BaseModel, ConfigDict


class ImagemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    imovel_id: int
    arquivo: str
    principal: bool
    ordem: int
    url: str | None = None


class ImagemUpdate(BaseModel):
    principal: bool | None = None
    ordem: int | None = None

