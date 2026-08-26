"""allow optional imovel fields

Revision ID: 0003_optional_imovel_fields
Revises: 0002_add_destacado
Create Date: 2026-08-26
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003_optional_imovel_fields"
down_revision: Union[str, None] = "0002_add_destacado"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


OPTIONAL_COLUMNS = (
    "descricao_curta",
    "descricao",
    "preco",
    "cidade",
    "bairro",
    "endereco",
    "tipo",
    "area",
    "quartos",
    "banheiros",
    "garagem",
)


def upgrade() -> None:
    for column in OPTIONAL_COLUMNS:
        op.alter_column("imoveis", column, existing_type=_column_type(column), nullable=True)


def downgrade() -> None:
    # Existing NULL values must be resolved before downgrading this migration.
    for column in OPTIONAL_COLUMNS:
        op.alter_column("imoveis", column, existing_type=_column_type(column), nullable=False)


def _column_type(column: str) -> sa.types.TypeEngine:
    types: dict[str, sa.types.TypeEngine] = {
        "descricao_curta": sa.String(length=300),
        "descricao": sa.Text(),
        "preco": sa.Numeric(12, 2),
        "cidade": sa.String(length=120),
        "bairro": sa.String(length=120),
        "endereco": sa.String(length=255),
        "tipo": sa.String(length=80),
        "area": sa.Integer(),
        "quartos": sa.Integer(),
        "banheiros": sa.Integer(),
        "garagem": sa.Integer(),
    }
    return types[column]
