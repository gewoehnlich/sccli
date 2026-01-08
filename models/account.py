from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.model import Model


class Account(Model):
    __tablename__ = "accounts"

    client_id: Mapped[str] = mapped_column(
        String,
        primary_key = True,
    )
    client_secret: Mapped[str] = mapped_column(
        String,
    )
    access_token: Mapped[str] = mapped_column(
        String,
    )
    refresh_token: Mapped[str] = mapped_column(
        String,
    )
    expire_timestamp: Mapped[int] = mapped_column(
        Integer,
    )

    def __repr__(self) -> str:
        return f"<Account(client_id={self.client_id}')>"
