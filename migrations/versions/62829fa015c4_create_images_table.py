"""create_images_table

Revision ID: 62829fa015c4
Revises: 7a80d8cef50a
Create Date: 2026-11-03 15:14:26.036224

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62829fa015c4'
down_revision: Union[str, Sequence[str], None] = '7a80d8cef50a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "images",
        sa.Column("url", sa.String, primary_key=True),
        sa.Column("data", sa.LargeBinary, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("images")
