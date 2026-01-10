from abc import abstractmethod
from typing import Protocol
from sqlalchemy.orm import Session, sessionmaker

from di.models_container import ModelsContainer


class Database(
    Protocol
):
    database_name: str
    models: ModelsContainer

    # @abstractmethod
    # def session_factory(
    #     self,
    # ) -> sessionmaker[Session]:
    #     ...

    @abstractmethod
    def initialize_tables(
        self,
    ) -> None:
        ...
