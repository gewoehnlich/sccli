from typing import Self
from dependency_injector import containers, providers

from core.auth              import Auth
from core.database          import Database
from core.server            import Server
# from di.actions_container   import ActionsContainer
from di.auth_requests_container import AuthRequestsContainer
# from di.commands_container  import CommandsContainer
# from di.dto_container       import DtoContainer
# from di.models_container    import ModelsContainer
# from di.requests_container  import RequestsContainer
# from di.resources_container import ResourcesContainer
from di.tables_container    import TablesContainer


class DiContainer(
    containers.DeclarativeContainer
):
    config = providers.Configuration()

    database = providers.Singleton(
        Database,
        database_name = config.database.name,
        tables = providers.Singleton(
            TablesContainer,
        )
    )

    # dto = providers.Singleton(
    #     DtoContainer,
    # )

    auth_requests = providers.Singleton(
        AuthRequestsContainer
    )
    auth = providers.Singleton(
        Auth,
        client_id     = config.soundcloud.client_id,
        client_secret = config.soundcloud.client_secret,
        server        = providers.Singleton(
            Server,
            server_port = config.server.port,
            server_path = config.server.path,
        ),
        authentication_request = auth_requests().authentication.provider,
        refresh_token_request = auth_requests().refresh_token.provider,
    )
    #
    # models = providers.Singleton(
    #     ModelsContainer,
    #     db_models  = tables,
    #     dto_models = dto,
    # )
    # requests = providers.Singleton(
    #     RequestsContainer,
    #     auth = auth,
    #     dto  = dto,
    # )
    # actions = providers.Singleton(
    #     ActionsContainer,
    #     requests = requests,
    #     database = database,
    #     tables   = tables,
    # )
    # resources = providers.Singleton(
    #     ResourcesContainer,
    # )
    # commands = providers.Singleton(
    #     CommandsContainer,
    #     actions   = actions,
    #     resources = resources,
    # )


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
