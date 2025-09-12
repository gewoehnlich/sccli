from dependency_injector import containers, providers
from typing import Self

from core.auth import Auth
from core.database import Database
from core.query_builder import QueryBuilder
from core.server import Server
from di.actions_container import ActionsContainer
from di.commands_container import CommandsContainer
# from di.dto_container import DtoContainer
from di.requests_container import RequestsContainer
from di.tables_container import TablesContainer
from di.resources_container import ResourcesContainer


class DiContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    query_builder = providers.Singleton(QueryBuilder)
    tables        = providers.Singleton(TablesContainer)

    db = providers.Singleton(
        Database,
        database_name = config.database_name,
        tables        = tables,
        query_builder = query_builder,
    )

    # dto       = providers.Singleton(DtoContainer)
    requests  = providers.Singleton(RequestsContainer)
    actions   = providers.Singleton(ActionsContainer)
    resources = providers.Singleton(ResourcesContainer)
    commands  = providers.Singleton(
        CommandsContainer,
        requests = requests,
        actions = actions,
        resources = resources,
    )

    server = providers.Singleton(
        Server,
        server_port = config.server_port,
        server_path = config.server_path,
    )
    auth = providers.Singleton(
        Auth,
        client_id     = config.client_id(),
        client_secret = config.client_secret(),
        redirect_uri  = config.redirect_uri(),
        tokens_file   = config.tokens_file(),
        # tokensDto = dto().tokens,
        server = server,
        authentication_request = requests().authentication,
        refresh_token_request  = requests().refresh_token,
    )

    _instance:    Self | None = None
    _initialized: bool        = False

    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        self._initialized = True
