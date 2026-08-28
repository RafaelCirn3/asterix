"""backfill commercial data for existing properties

Revision ID: 0005_backfill_dados_comerciais
Revises: 0004_add_tipo_anuncio_numero
Create Date: 2026-08-27
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0005_backfill_dados_comerciais"
down_revision: Union[str, None] = "0004_add_tipo_anuncio_numero"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DEFAULT_TIPO_ANUNCIO = "Venda"
DEFAULT_NUMERO = "556181200528"


def upgrade() -> None:
    op.execute(
        sa.text(
            "UPDATE imoveis SET tipo_anuncio = :tipo_anuncio "
            "WHERE tipo_anuncio IS NULL OR btrim(tipo_anuncio) = ''"
        ).bindparams(tipo_anuncio=DEFAULT_TIPO_ANUNCIO)
    )
    op.execute(
        sa.text(
            "UPDATE imoveis SET numero = :numero "
            "WHERE numero IS NULL OR btrim(numero) = ''"
        ).bindparams(numero=DEFAULT_NUMERO)
    )


def downgrade() -> None:
    # O backfill substitui valores ausentes por dados editáveis; não é seguro
    # inferir quais registros eram originalmente NULL durante o downgrade.
    pass
