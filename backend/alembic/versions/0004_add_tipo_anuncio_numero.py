"""add tipo anuncio and corretor numero

Revision ID: 0004_add_tipo_anuncio_numero
Revises: 0003_optional_imovel_fields
Create Date: 2026-08-27
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0004_add_tipo_anuncio_numero"
down_revision: Union[str, None] = "0003_optional_imovel_fields"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DEFAULT_TIPO_ANUNCIO = "Venda"
DEFAULT_NUMERO = "556181200528"


def upgrade() -> None:
    op.add_column("imoveis", sa.Column("tipo_anuncio", sa.String(length=20), nullable=True))
    op.add_column("imoveis", sa.Column("numero", sa.String(length=30), nullable=True))
    op.create_index(op.f("ix_imoveis_tipo_anuncio"), "imoveis", ["tipo_anuncio"], unique=False)

    # Compatibilidade com os imóveis cadastrados antes desta migration.
    # Os valores são apenas um preenchimento inicial e podem ser editados normalmente depois.
    op.execute(
        sa.text(
            "UPDATE imoveis "
            "SET tipo_anuncio = :tipo_anuncio "
            "WHERE tipo_anuncio IS NULL"
        ).bindparams(tipo_anuncio=DEFAULT_TIPO_ANUNCIO)
    )
    op.execute(
        sa.text(
            "UPDATE imoveis "
            "SET numero = :numero "
            "WHERE numero IS NULL"
        ).bindparams(numero=DEFAULT_NUMERO)
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_imoveis_tipo_anuncio"), table_name="imoveis")
    op.drop_column("imoveis", "numero")
    op.drop_column("imoveis", "tipo_anuncio")
