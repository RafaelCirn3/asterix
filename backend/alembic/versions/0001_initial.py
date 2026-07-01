"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-07-01
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_table(
        "imoveis",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nome", sa.String(length=180), nullable=False, index=True),
        sa.Column("descricao_curta", sa.String(length=300), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=False),
        sa.Column("preco", sa.Numeric(12, 2), nullable=False),
        sa.Column("cidade", sa.String(length=120), nullable=False, index=True),
        sa.Column("bairro", sa.String(length=120), nullable=False, index=True),
        sa.Column("endereco", sa.String(length=255), nullable=False),
        sa.Column("tipo", sa.String(length=80), nullable=False, index=True),
        sa.Column("area", sa.Integer(), nullable=False),
        sa.Column("quartos", sa.Integer(), nullable=False),
        sa.Column("banheiros", sa.Integer(), nullable=False),
        sa.Column("garagem", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="Disponivel", index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_table(
        "imagens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("imovel_id", sa.Integer(), sa.ForeignKey("imoveis.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("arquivo", sa.String(length=255), nullable=False),
        sa.Column("principal", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("ordem", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_table("imagens")
    op.drop_table("imoveis")
    op.drop_table("usuarios")

