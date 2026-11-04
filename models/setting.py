from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

from core.model import Model


class Setting(Model):
    __tablename__ = "settings"

    name: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str] = mapped_column(String)
