from dependency_injector import containers, providers
from typing import Self

from core.auth     import Auth
from core.database import Database
from core.server   import Server
from di.actions_container       import ActionsContainer
from di.auth_requests_container import AuthRequestsContainer
from di.commands_container      import CommandsContainer
from di.dto_container           import DtoContainer
from di.models_container        import ModelsContainer
from di.requests_container      import RequestsContainer
from di.resources_container     import ResourcesContainer
from di.tables_container        import TablesContainer


class DiContainer(
    containers.DeclarativeContainer
):
    config = providers.Configuration()

    tables = providers.Singleton(
        TablesContainer,
    )
    database = providers.Singleton(
        Database,
    )

    dto = providers.Singleton(
        DtoContainer,
    )

    server = providers.Singleton(
        Server,
    )
    auth_requests = providers.Singleton(
        AuthRequestsContainer,
    )
    auth = providers.Singleton(
        Auth,
    )

    models = providers.Singleton(
        ModelsContainer,
    )
    requests = providers.Singleton(
        RequestsContainer,
    )
    actions = providers.Singleton(
        ActionsContainer,
    )
    resources = providers.Singleton(
        ResourcesContainer,
    )
    commands = providers.Singleton(
        CommandsContainer,
    )


    _instance:    Self | None = None
    _initialized: bool        = False

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
    ) -> None:
        if self._initialized:
            return

        self._initialized = True
