from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Text

from core.model import Model


class User(Model):
    __tablename__: str = "users"

    avatar_url: Mapped[str | None] = mapped_column(
        String,
    )
    city: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    country: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )
    created_at: Mapped[str] = mapped_column(
        String,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    permalink: Mapped[str] = mapped_column(
        String,
    )
    permalink_url: Mapped[str] = mapped_column(
        String,
    )
    username: Mapped[str] = mapped_column(
        String,
    )

    def __repr__(self) -> str:
        return f"<UsersTable(id={self.id}, username='{self.username}')>"

    @property
    def urn(self) -> str:
        return f"soundcloud:users:{self.id}"
