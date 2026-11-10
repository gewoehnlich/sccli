"""add track streams to tracks table

Revision ID: 1f4aae9024e0
Revises: 78beaf4ae38f
Create Date: 2026-11-10 23:35:25.911460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f4aae9024e0'
down_revision: Union[str, Sequence[str], None] = '78beaf4ae38f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "tracks",
        sa.Column("streams", sa.JSON, nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("tracks", "streams")
