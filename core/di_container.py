from dependency_injector import containers, providers
from typing import Self
# from di.actions_container import ActionsContainer
# from di.auth_container import AuthContainer
# from di.commands_container import CommandsContainer
# from di.database_container import DatabaseContainer
# from di.query_builder_container import QueryBuilderContainer
# from di.requests_container import RequestsContainer
# from di.server_container import ServerContainer
from di.tables_container import TablesContainer
# from di.resources_container import ResourcesContainer
from core.query_builder import QueryBuilder
from core.database import Database

class DiContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    query_builder = providers.Singleton(QueryBuilder)
    tables = providers.Singleton(TablesContainer)
    db = providers.Singleton(
        Database,
        database_name = config.database_name,
        tables = tables,
        query_builder = query_builder,
    )

    # requests  = providers.Singleton(RequestsContainer)
    # resources = providers.Singleton(ResourcesContainer)
    # actions   = providers.Singleton(ActionsContainer)
    # commands  = providers.Singleton(CommandsContainer)
    #
    # auth = providers.Singleton(
    #     AuthContainer,
    #     client_id     = config.client_id,
    #     client_secret = config.client_secret,
    #     redirect_uri  = config.redirect_uri,
    #     tokens_file   = ".tokens.json",
    # )
    #
    # server = providers.Singleton(
    #     ServerContainer,
    #     server_port = config.server_port,
    #     server_path = config.server_path,
    # )

    _instance: Self | None = None
    _initialized: bool = False

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        self._initialized = True
