"""add cascade delete to training plan fks

Revision ID: a1b2c3d4e5f6
Revises: 7b868150e879
Create Date: 2026-02-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '7b868150e879'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # training_plan_exercises.training_plan_id
    op.drop_constraint('training_plan_exercises_training_plan_id_fkey', 'training_plan_exercises', type_='foreignkey')
    op.create_foreign_key(
        'training_plan_exercises_training_plan_id_fkey',
        'training_plan_exercises', 'training_plans',
        ['training_plan_id'], ['id'],
        ondelete='CASCADE'
    )

    # training_sessions.training_plan_id
    op.drop_constraint('training_sessions_training_plan_id_fkey', 'training_sessions', type_='foreignkey')
    op.create_foreign_key(
        'training_sessions_training_plan_id_fkey',
        'training_sessions', 'training_plans',
        ['training_plan_id'], ['id'],
        ondelete='CASCADE'
    )

    # training_executions.training_session_id
    op.drop_constraint('training_executions_training_session_id_fkey', 'training_executions', type_='foreignkey')
    op.create_foreign_key(
        'training_executions_training_session_id_fkey',
        'training_executions', 'training_sessions',
        ['training_session_id'], ['id'],
        ondelete='CASCADE'
    )

    # training_executions.training_plan_exercise_id
    op.drop_constraint('training_executions_training_plan_exercise_id_fkey', 'training_executions', type_='foreignkey')
    op.create_foreign_key(
        'training_executions_training_plan_exercise_id_fkey',
        'training_executions', 'training_plan_exercises',
        ['training_plan_exercise_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # training_executions.training_plan_exercise_id
    op.drop_constraint('training_executions_training_plan_exercise_id_fkey', 'training_executions', type_='foreignkey')
    op.create_foreign_key(
        'training_executions_training_plan_exercise_id_fkey',
        'training_executions', 'training_plan_exercises',
        ['training_plan_exercise_id'], ['id']
    )

    # training_executions.training_session_id
    op.drop_constraint('training_executions_training_session_id_fkey', 'training_executions', type_='foreignkey')
    op.create_foreign_key(
        'training_executions_training_session_id_fkey',
        'training_executions', 'training_sessions',
        ['training_session_id'], ['id']
    )

    # training_sessions.training_plan_id
    op.drop_constraint('training_sessions_training_plan_id_fkey', 'training_sessions', type_='foreignkey')
    op.create_foreign_key(
        'training_sessions_training_plan_id_fkey',
        'training_sessions', 'training_plans',
        ['training_plan_id'], ['id']
    )

    # training_plan_exercises.training_plan_id
    op.drop_constraint('training_plan_exercises_training_plan_id_fkey', 'training_plan_exercises', type_='foreignkey')
    op.create_foreign_key(
        'training_plan_exercises_training_plan_id_fkey',
        'training_plan_exercises', 'training_plans',
        ['training_plan_id'], ['id']
    )
