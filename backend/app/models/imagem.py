from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Imagem(Base):
    __tablename__ = "imagens"

    id: Mapped[int] = mapped_column(primary_key=True)
    imovel_id: Mapped[int] = mapped_column(ForeignKey("imoveis.id", ondelete="CASCADE"), index=True)
    arquivo: Mapped[str] = mapped_column(String(255))
    principal: Mapped[bool] = mapped_column(Boolean, default=False)
    ordem: Mapped[int] = mapped_column(Integer, default=0)

    imovel = relationship("Imovel", back_populates="imagens")

