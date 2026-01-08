from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.table import Table


class TokensTable(
    Table
):
    __tablename__ = "tokens"

    client_id: Mapped[str] = mapped_column(
        String,
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
        return f"<TracksTable(client_id={self.client_id}')>"
