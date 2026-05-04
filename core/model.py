from typing import Any
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    @classmethod
    def primary_key(
        cls,
    ) -> str:
        return cls.__mapper__.primary_key[0].name

    @classmethod
    def columns(
        cls,
    ) -> list[str]:
        return cls.__mapper__.columns.keys()

    def to_tuple(
        self,
    ) -> tuple[Any]:
        return tuple(getattr(self, attr.key) for attr in inspect(self).mapper.column_attrs)
