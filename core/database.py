from typing import Self
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import sqlalchemy

from core.dto import Dto
from core.model import Model
from di.models_container import ModelsContainer


class Database:
    _instance: Self | None = None
    _initialized: bool = False


    def __new__(
        cls: type[Self],
        *args,
        **kwargs,
    ) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def __init__(
        self,
        database_name: str,
        models:        ModelsContainer,
    ) -> None:
        if self._initialized:
            return

        self.database_name: str = database_name

        self.engine: sqlalchemy.Engine = sqlalchemy.create_engine(
            f"sqlite+pysqlite:///{self.database_name}"
        )

        self.session_factory = sessionmaker(
            bind = self.engine,
            expire_on_commit = False,
        )

        self.models:     ModelsContainer = models 
        self.model_base: DeclarativeBase = self.models.model()

        self._initialized = True


    def initialize_tables(
        self,
    ) -> None:
        self.model_base.metadata.create_all(self.engine)


    def insert(
        self,
        model: Model,
    ) -> None:
        with sessionmaker(bind = self.engine) as session:
            session.add(model)
            session.commit()
