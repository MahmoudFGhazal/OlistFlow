"""seed_states

Revision ID: 65df28bdeae2
Revises: 8afababec81a
Create Date: 2026-08-12 19:32:15.651813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65df28bdeae2'
down_revision: Union[str, Sequence[str], None] = '8afababec81a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

states_table = sa.table(
    'states',
    sa.column('sta_name', sa.String),
    sa.column('sta_uf', sa.String),
    schema='core'
)

STATES = [
    ('Acre', 'AC'), ('Alagoas', 'AL'), ('Amapá', 'AP'), ('Amazonas', 'AM'),
    ('Bahia', 'BA'), ('Ceará', 'CE'), ('Distrito Federal', 'DF'), ('Espírito Santo', 'ES'),
    ('Goiás', 'GO'), ('Maranhão', 'MA'), ('Mato Grosso', 'MT'), ('Mato Grosso do Sul', 'MS'),
    ('Minas Gerais', 'MG'), ('Pará', 'PA'), ('Paraíba', 'PB'), ('Paraná', 'PR'),
    ('Pernambuco', 'PE'), ('Piauí', 'PI'), ('Rio de Janeiro', 'RJ'), ('Rio Grande do Norte', 'RN'),
    ('Rio Grande do Sul', 'RS'), ('Rondônia', 'RO'), ('Roraima', 'RR'), ('Santa Catarina', 'SC'),
    ('São Paulo', 'SP'), ('Sergipe', 'SE'), ('Tocantins', 'TO'),
]

def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(states_table, [
        {'sta_name': name, 'sta_uf': uf} for name, uf in STATES
    ])


def downgrade() -> None:
    """Downgrade schema."""
    op.bulk_delete(states_table, [
        {'sta_name': name, 'sta_uf': uf} for name, uf in STATES
    ])
