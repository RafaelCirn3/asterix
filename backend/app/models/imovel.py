from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Imovel(Base):
    __tablename__ = "imoveis"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(180), index=True)
    descricao_curta: Mapped[str] = mapped_column(String(300))
    descricao: Mapped[str] = mapped_column(Text)
    preco: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    cidade: Mapped[str] = mapped_column(String(120), index=True)
    bairro: Mapped[str] = mapped_column(String(120), index=True)
    endereco: Mapped[str] = mapped_column(String(255))
    tipo: Mapped[str] = mapped_column(String(80), index=True)
    area: Mapped[int] = mapped_column(Integer)
    quartos: Mapped[int] = mapped_column(Integer)
    banheiros: Mapped[int] = mapped_column(Integer)
    garagem: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30), default="Disponivel", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    imagens = relationship("Imagem", back_populates="imovel", cascade="all, delete-orphan", order_by="Imagem.ordem")

