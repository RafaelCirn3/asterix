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


def upgrade() -> None:
    op.add_column("imoveis", sa.Column("tipo_anuncio", sa.String(length=20), nullable=True))
    op.add_column("imoveis", sa.Column("numero", sa.String(length=30), nullable=True))
    op.create_index(op.f("ix_imoveis_tipo_anuncio"), "imoveis", ["tipo_anuncio"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_imoveis_tipo_anuncio"), table_name="imoveis")
    op.drop_column("imoveis", "numero")
    op.drop_column("imoveis", "tipo_anuncio")
