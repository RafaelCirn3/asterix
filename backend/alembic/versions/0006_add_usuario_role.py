"""add user role for RBAC

Revision ID: 0006_add_usuario_role
Revises: 0005_backfill_dados_comerciais
Create Date: 2026-09-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0006_add_usuario_role"
down_revision: Union[str, None] = "0005_backfill_dados_comerciais"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("usuarios", sa.Column("role", sa.String(length=32), nullable=False, server_default="editor"))
    op.create_index(op.f("ix_usuarios_role"), "usuarios", ["role"], unique=False)
    op.execute(sa.text("UPDATE usuarios SET role = 'admin' WHERE email = 'admin@asterix.com.br'"))
    op.alter_column("usuarios", "role", server_default=None)


def downgrade() -> None:
    op.drop_index(op.f("ix_usuarios_role"), table_name="usuarios")
    op.drop_column("usuarios", "role")
