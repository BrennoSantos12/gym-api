"""add unique constraint to exercises name

Revision ID: f3a9c0b1d2e4
Revises: 1302e57b71a3
Create Date: 2026-03-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'f3a9c0b1d2e4'
down_revision: Union[str, Sequence[str], None] = '1302e57b71a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('uq_exercises_name', 'exercises', ['name'])


def downgrade() -> None:
    op.drop_constraint('uq_exercises_name', 'exercises', type_='unique')
