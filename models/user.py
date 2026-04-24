from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, String, Text

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
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    followers_count: Mapped[int] = mapped_column(
        Integer,
    )
    followings_count: Mapped[int] = mapped_column(
        Integer,
    )
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    last_modified: Mapped[datetime] = mapped_column(
        DateTime,
    )
    permalink: Mapped[str] = mapped_column(
        String,
    )
    permalink_url: Mapped[str] = mapped_column(
        String,
    )
    playlists_count: Mapped[int] = mapped_column(
        Integer,
    )
    public_favorites_count: Mapped[int] = mapped_column(
        Integer,
    )
    reposts_count: Mapped[int] = mapped_column(
        Integer,
    )
    track_count: Mapped[int] = mapped_column(
        Integer,
    )
    uri: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    urn: Mapped[str] = mapped_column(
        String,
    )
    username: Mapped[str] = mapped_column(
        String,
    )

    def __repr__(self) -> str:
        return f"<UsersTable(id={self.id}, username='{self.username}')>"
