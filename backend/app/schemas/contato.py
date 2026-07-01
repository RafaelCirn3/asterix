from pydantic import BaseModel, EmailStr, Field


class ContatoCreate(BaseModel):
    nome: str = Field(min_length=2)
    email: EmailStr
    telefone: str = Field(min_length=8)
    mensagem: str = Field(min_length=10)


class ContatoRead(ContatoCreate):
    recebido: bool = True

