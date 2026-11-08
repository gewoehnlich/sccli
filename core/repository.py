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

    async def get(self, **kwargs: dict[str, Any]) -> Sequence[ModelT]:
        async with self._database.session() as session:
            stmt = select(self.model).filter_by(**kwargs)

            result = await session.execute(stmt)

            return result.scalars().all()

    async def get_one(self, primary_key: str | int) -> ModelT | None:
        async with self._database.session() as session:
            return await session.get(self.model, primary_key)

    async def store(self, model: ModelT) -> ModelT:
        async with self._database.session() as session:
            merged = await session.merge(model)
            await session.flush()

            return merged

    async def store_many(self, models: Sequence[ModelT]) -> None:
        async with self._database.session() as session:
            for model in models:
                await session.merge(model)

    async def delete(self, model: ModelT) -> bool:
        async with self._database.session() as session:
            attached = await session.merge(model)
            await session.delete(attached)

            return True
