"""add revoked tokens table

Revision ID: 0007_add_revoked_tokens
Revises: 0006_add_usuario_role
Create Date: 2026-09-05
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0007_add_revoked_tokens"
down_revision: Union[str, None] = "0006_add_usuario_role"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tokens_revogados",
        sa.Column("jti", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("jti"),
    )
    op.create_index(op.f("ix_tokens_revogados_expires_at"), "tokens_revogados", ["expires_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tokens_revogados_expires_at"), table_name="tokens_revogados")
    op.drop_table("tokens_revogados")
