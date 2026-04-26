from typing import Any
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    def __init__(
        self,
        **kwargs: dict[str, Any],
    ) -> None:
        pass

    @classmethod
    def primary_key(
        cls,
    ) -> str:
        return cls.__mapper__.primary_key[0].name
