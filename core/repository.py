from collections.abc import Sequence
from typing import Any

from sqlalchemy import select

from core.database import Database
from core.model import Model


class Repository[ModelT: Model]:
    model: type[ModelT]

    def __init__(
        self,
        database: Database,
    ) -> None:
        self._database: Database = database

    def get(
        self,
        **kwargs: dict[str, Any],
    ) -> Sequence[ModelT]:
        with self._database.session() as session:
            stmt = select(self.model).filter_by(**kwargs)

            return session.execute(stmt).scalars().all()

    def get_one(
        self,
        key: str | int,
    ) -> ModelT | None:
        with self._database.session() as session:
            return session.get(self.model, key)

    def store(
        self,
        model: ModelT,
    ) -> ModelT:
        with self._database.session() as session:
            merged = session.merge(model)  # insert or update by primary key
            session.flush()

            return merged

    def delete(
        self,
        model: ModelT,
    ) -> bool:
        with self._database.session() as session:
            session.delete(model)

            return True
