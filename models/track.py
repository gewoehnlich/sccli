from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import Model

if TYPE_CHECKING:
    from models.user import User


class Track(Model):
    __tablename__ = "tracks"

    artwork_url: Mapped[str | None] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration: Mapped[int] = mapped_column(Integer)
    id: Mapped[int] = mapped_column(primary_key=True)
    permalink_url: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(
        back_populates="tracks",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"<Track(id={self.id}, title='{self.title}')>"

    @property
    def urn(self) -> str:
        return f"soundcloud:tracks:{self.id}"

    @property
    def formatted_duration(self) -> str:
        minutes, seconds = divmod(self.duration, 60)

        return f"{minutes}:{seconds:02d}"

    @property
    def artwork_url_large(self) -> str | None:
        if not self.artwork_url:
            return None

        return self.artwork_url.replace("-large", "-t500x500")

    @staticmethod
    def from_api(data: dict[str, Any], user_id: int) -> Track:
        return Track(
            artwork_url=data["artwork_url"],
            created_at=data["created_at"],
            description=data["description"],
            duration=data["duration"],
            id=data["id"],
            permalink_url=data["permalink_url"],
            title=data["title"],
            user_id=user_id,
        )
