"""add destacado to imoveis

Revision ID: 0002_add_destacado
Revises: 0001_initial
Create Date: 2026-08-25
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002_add_destacado"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "imoveis",
        sa.Column("destacado", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_index("ix_imoveis_destacado", "imoveis", ["destacado"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_imoveis_destacado", table_name="imoveis")
    op.drop_column("imoveis", "destacado")
