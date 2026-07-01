from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioBase(BaseModel):
    nome: str = Field(min_length=2, max_length=160)
    email: EmailStr
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=6)


class UsuarioUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    senha: str | None = Field(default=None, min_length=6)
    ativo: bool | None = None


class UsuarioRead(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

