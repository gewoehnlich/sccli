from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Boolean

from core.model import Model


class Track(Model):
    __tablename__ = "tracks"

    access: Mapped[str] = mapped_column(
        String,
    )
    artwork_url: Mapped[str | None] = mapped_column(
        String,
    )
    created_at: Mapped[str] = mapped_column(
        String,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    duration: Mapped[int] = mapped_column(
        Integer,
    )
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    permalink_url: Mapped[str] = mapped_column(
        String,
    )
    title: Mapped[str] = mapped_column(
        String,
    )
    uri: Mapped[str] = mapped_column(
        String,
        unique=True,
    )
    urn: Mapped[str] = mapped_column(
        String,
    )
    user_favorite: Mapped[bool] = mapped_column(
        Boolean,
    )
    user_playback_count: Mapped[int] = mapped_column(
        Integer,
    )

    def __repr__(self) -> str:
        return f"<Track(id={self.id}, title='{self.title}')>"
