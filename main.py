from typing import Self
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from core.auth              import Auth
from core.database          import Database
from core.server            import Server
from core.settings          import Settings
from default_settings.app   import AppSettings
from di.actions_container   import ActionsContainer
from di.commands_container  import CommandsContainer
from di.dto_container       import DtoContainer
from di.models_container    import ModelsContainer
from di.requests_container  import RequestsContainer
from di.resources_container import ResourcesContainer
from di.tables_container    import TablesContainer


class DiContainer(
    containers.DeclarativeContainer
):
    config = providers.Configuration()

    tables = providers.Singleton(
        TablesContainer,
    )
    database = providers.Singleton(
        Database,
        database_name = config.database.name,
        tables = tables,
    )

    dto = providers.Singleton(
        DtoContainer,
    )

    server = providers.Singleton(
        Server,
        server_port = config.server.port,
        server_path = config.server.path,
    )
    auth = providers.Singleton(
        Auth,
        client_id     = config.soundcloud.client_id,
        client_secret = config.soundcloud.client_secret,
        server_port   = config.server.port,
        server_path   = config.server.path,
        tokens_file   = config.tokens.file,
        server        = server,
        auth_requests = auth_requests,
    )

    models = providers.Singleton(
        ModelsContainer,
        db_models  = tables,
        dto_models = dto,
    )
    requests = providers.Singleton(
        RequestsContainer,
        auth = auth,
        dto  = dto,
    )
    actions = providers.Singleton(
        ActionsContainer,
        requests = requests,
        database = database,
        tables   = tables,
    )
    resources = providers.Singleton(
        ResourcesContainer,
    )
    commands = providers.Singleton(
        CommandsContainer,
        actions   = actions,
        resources = resources,
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


@inject
def main(
    di_container: DiContainer = Provide[DiContainer],
) -> None:
    di_container.commands().welcome().run()
    # di_container.commands().my_liked_tracks().run()


if __name__ == "__main__":
    settings: AppSettings = Settings().load()

    di_container: DiContainer = DiContainer()
    di_container.config.from_pydantic(
        settings = settings,
    )

    di_container.database().initialize_tables()

    di_container.wire(
        modules = [__name__],
    )

    main()
