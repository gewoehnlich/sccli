"""create tracks table

Revision ID: 7a80d8cef50a
Revises: 2380ab3375d9
Create Date: 2026-10-11 00:28:30.790498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a80d8cef50a'
down_revision: Union[str, Sequence[str], None] = '2380ab3375d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tracks",
        sa.Column("artwork_url", sa.String, nullable=True),
        sa.Column("created_at", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("duration", sa.Integer, nullable=False),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("permalink_url", sa.String, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tracks")
