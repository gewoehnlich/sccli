from typing import Any, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.model import Model


class Repository:
    def __init__(
        self,
        model: type[Model],
        session_factory: type[Session],
    ) -> None:
        self.model = model
        self.session_factory = session_factory

    def get(
        self,
        **kwargs: dict[str, Any],
    ) -> Sequence[Model]:
        with self.session_factory() as session:
            stmt = select(self.model).filter_by(**kwargs)
            return session.execute(stmt).scalars().all()

    def store(
        self,
        **kwargs: dict[str, Any],
    ) -> Model:
        with self.session_factory() as session:
            model = session.get_one(self.model, kwargs[self.model.primary_key()])

            if not model:
                model = self.model(**kwargs)

                session.add(instance=model)
            else:
                for field, value in kwargs.items():
                    setattr(model, field, value)

            session.commit()

            return model

    def delete(
        self,
        **kwargs: dict[str, Any],
    ) -> bool:
        with self.session_factory() as session:
            model = session.get_one(self.model, kwargs[self.model.primary_key()])

            if not model:
                raise ValueError(f"{self.model} not found")

            session.delete(model)
            session.commit()

        return True
