from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Imovel(Base):
    __tablename__ = "imoveis"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(180), index=True)
    descricao_curta: Mapped[str | None] = mapped_column(String(300), nullable=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    preco: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    cidade: Mapped[str | None] = mapped_column(String(120), index=True, nullable=True)
    bairro: Mapped[str | None] = mapped_column(String(120), index=True, nullable=True)
    endereco: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tipo: Mapped[str | None] = mapped_column(String(80), index=True, nullable=True)
    area: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quartos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    banheiros: Mapped[int | None] = mapped_column(Integer, nullable=True)
    garagem: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Disponivel", index=True)
    destacado: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    imagens = relationship("Imagem", back_populates="imovel", cascade="all, delete-orphan", order_by="Imagem.ordem")
