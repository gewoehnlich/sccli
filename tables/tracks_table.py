from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Boolean

from core.table import Table
from enums.track_access import TrackAccessEnum


class TracksTable(Table):
    __tablename__ = "tracks"

    access: Mapped[TrackAccessEnum] = mapped_column(
        Enum(TrackAccessEnum),
    )
    artwork_url: Mapped[Optional[str]] = mapped_column(
        String,
    )
    comments_count: Mapped[int] = mapped_column(
        Integer,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable = True,
    )
    duration: Mapped[int] = mapped_column(
        Integer,
    )
    favoritings_count: Mapped[int] = mapped_column(
        Integer,
    )
    id: Mapped[int] = mapped_column(
        primary_key = True,
        nullable = False,
    )
    metadata_artist: Mapped[Optional[str]] = mapped_column(
        String,
        nullable = True,
    )
    permalink_url: Mapped[str] = mapped_column(
        String,
    )
    playback_count: Mapped[int] = mapped_column(
        Integer,
    )
    reposts_count: Mapped[int] = mapped_column(
        Integer,
    )
    stream_url: Mapped[str] = mapped_column(
        String,
    )
    title: Mapped[str] = mapped_column(
        String,
    )
    uri: Mapped[str] = mapped_column(
        String,
        unique = True,
    )
    urn: Mapped[str] = mapped_column(
        String,
    )
    # user: Mapped[User]
    user_favorite: Mapped[bool] = mapped_column(
        Boolean,
    )
    user_playback_count: Mapped[int] = mapped_column(
        Integer,
    )


    def __repr__(self) -> str:
        return f"<TracksTable(id={self.id}, title='{self.title}')>"
