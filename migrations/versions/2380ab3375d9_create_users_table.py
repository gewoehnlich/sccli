"""create users table

Revision ID: 2380ab3375d9
Revises: 19b6e534da02
Create Date: 2026-10-11 00:36:08.113895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2380ab3375d9'
down_revision: Union[str, Sequence[str], None] = '19b6e534da02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("avatar_url", sa.String, nullable=True),
        sa.Column("city", sa.String, nullable=True),
        sa.Column("country", sa.String, nullable=True),
        sa.Column("created_at", sa.String, nullable=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("permalink", sa.String, nullable=False),
        sa.Column("permalink_url", sa.String, nullable=False),
        sa.Column("username", sa.String, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
