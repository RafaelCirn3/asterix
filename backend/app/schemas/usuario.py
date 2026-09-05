from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

UserRole = Literal["admin", "editor"]


class UsuarioBase(BaseModel):
    nome: str = Field(min_length=2, max_length=160)
    email: EmailStr
    ativo: bool = True
    role: UserRole = "editor"


class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=8)


class UsuarioUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=160)
    email: EmailStr | None = None
    senha: str | None = Field(default=None, min_length=8)
    ativo: bool | None = None
    role: UserRole | None = None


class UsuarioRead(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
