from typing import Self
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import sqlalchemy

from core.dto import Dto
from di.tables_container import TablesContainer


class Database:
    database_name: str = ""

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
        tables:        TablesContainer,
    ) -> None:
        if self._initialized:
            return

        self.database_name: str = database_name

        self.engine: sqlalchemy.Engine = sqlalchemy.create_engine(
            f"sqlite+pysqlite:///{self.database_name}"
        )
        # self.session = sessionmaker(bind = self.engine)

        self.tables: TablesContainer = tables
        self.table_base: DeclarativeBase = self.tables.table_base()

        self._initialized = True

    def initialize_tables(
        self,
    ) -> None:
        self.table_base.metadata.create_all(self.engine)

    def insert(
        self,
        dto:   Dto,
    ) -> None:
        with sessionmaker(bind = self.engine) as session:
            session.add(dto)
            session.commit()
            print(session.query(dto).all())
