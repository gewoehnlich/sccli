"""create_settings_table

Revision ID: 78beaf4ae38f
Revises: 62829fa015c4
Create Date: 2026-11-04 23:57:19.021219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78beaf4ae38f'
down_revision: Union[str, Sequence[str], None] = '62829fa015c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "settings",
        sa.Column("name", sa.String, primary_key=True),
        sa.Column("value", sa.String)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("settings")
