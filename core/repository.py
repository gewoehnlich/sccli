from typing import Any, Callable, Sequence
from pydantic.main import ModelT
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from core.database import Database
from core.model import Model


class Repository:
    def __init__(
        self,
        model: type[Model],
        database: Database,
    ) -> None:
        self.model: type[Model] = model
        self._database: Database = database

    def get(
        self,
        **kwargs: dict[str, Any],
    ) -> Sequence[Model]:
        with self._database.session() as session:
            stmt = select(self.model).filter_by(**kwargs)
            return session.execute(stmt).scalars().all()

    def store(
        self,
        **kwargs: dict[str, Any],
    ) -> Model:
        with self._database.session() as session:
            try:
                model = session.get_one(self.model, kwargs[self.model.primary_key()])

                for field, value in kwargs.items():
                    setattr(model, field, value)

            except NoResultFound:
                model = self.model(**kwargs)

                session.add(instance=model)

            session.commit()

            return model

    def delete(
        self,
        **kwargs: dict[str, Any],
    ) -> bool:
        with self._database.session() as session:
            model = session.get_one(self.model, kwargs[self.model.primary_key()])

            if not model:
                raise ValueError(f"{self.model} not found")

            session.delete(model)
            session.commit()

        return True
