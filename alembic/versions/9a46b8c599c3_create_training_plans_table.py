"""create training_plans table

Revision ID: 9a46b8c599c3
Revises: 7bf8e6c2acf3
Create Date: 2026-02-11 21:27:49.519377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a46b8c599c3'
down_revision: Union[str, Sequence[str], None] = '7bf8e6c2acf3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'training_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('training_id', sa.Integer(), nullable=False),
        sa.Column('day_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['training_id'], ['trainings.id']),
        sa.ForeignKeyConstraint(['day_id'], ['days.id'])
    )
    op.create_index(op.f('ix_training_plans_id'), 'training_plans', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_training_plans_id'), table_name='training_plans')
    op.drop_table('training_plans')
