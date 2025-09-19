from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Integer, Text

from core.table import Table


class UsersTable(Table):
    __tablename__: str = "users"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        nullable = False,
    )
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String,
        nullable = True
    )
    city: Mapped[Optional[str]] = mapped_column(
        String,
        nullable = True
    )
    country: Mapped[Optional[str]] = mapped_column(
        String,
        nullable = True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable = True
    )
    followers_count: Mapped[int] = mapped_column(
        Integer
    )
    followings_count: Mapped[int] = mapped_column(
        Integer
    )
    kind: Mapped[Optional[str]] = mapped_column(
        String,
        nullable = True
    )
    last_modified: Mapped[datetime] = mapped_column(
        DateTime
    )
    permalink: Mapped[str] = mapped_column(
        String
    )
    permalink_url: Mapped[str] = mapped_column(
        String
    )
    plan: Mapped[str] = mapped_column(
        String
    )
    track_count: Mapped[int] = mapped_column(
        Integer,
    )
    uri: Mapped[str] = mapped_column(
        String,
        unique = True
    )
    urn: Mapped[str] = mapped_column(
        String
    )
    username: Mapped[str] = mapped_column(
        String
    )


    def __repr__(self) -> str:
        return f"<UsersTable(id={self.id}, username='{self.username}')>"
