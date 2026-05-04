from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.model import Model


class Track(Model):
    __tablename__ = "tracks"

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
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    def __repr__(self) -> str:
        return f"<Track(id={self.id}, title='{self.title}')>"

    @property
    def urn(self) -> str:
        return f"soundcloud:tracks:{self.id}"
