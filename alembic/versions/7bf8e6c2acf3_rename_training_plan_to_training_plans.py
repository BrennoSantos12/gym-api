"""rename training_plan to training_plans

Revision ID: 7bf8e6c2acf3
Revises: 7bf586d7d9e8
Create Date: 2026-02-11 21:25:31.493714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7bf8e6c2acf3'
down_revision: Union[str, Sequence[str], None] = '7bf586d7d9e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
