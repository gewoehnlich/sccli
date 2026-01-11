from typing import Self
from dependency_injector import containers, providers

from core.auth              import Auth
from core.server            import Server
from databases.sqlite_database import SqliteDatabase
# from di.actions_container   import ActionsContainer
from di.auth_requests_container import AuthRequestsContainer
# from di.commands_container  import CommandsContainer
# from di.dto_container       import DtoContainer
from di.models_container    import ModelsContainer
from di.repository_container import RepositoryContainer
# from di.requests_container  import RequestsContainer
# from di.resources_container import ResourcesContainer
# from di.tables_container    import TablesContainer


class DiContainer(
    containers.DeclarativeContainer
):
    config = providers.Configuration()

    database = providers.Singleton(
        SqliteDatabase,
        database_name = config.database.name,
        models = providers.Singleton(
            ModelsContainer,
        )
    )

    repositories = providers.Container(
        RepositoryContainer,
        session_factory = database.provided.session_factory,
    )

    auth_requests = providers.Singleton(
        AuthRequestsContainer
    )
    auth = providers.Singleton(
        Auth,
        client_id     = config.soundcloud.client_id,
        client_secret = config.soundcloud.client_secret,
        server        = providers.Singleton(
            Server,
            port = config.server.port,
            path = config.server.path,
        ),
        account_repository     = repositories().account,
        authentication_request = auth_requests().authentication.provider,
        refresh_token_request  = auth_requests().refresh_token.provider,
    )

    # dto = providers.Singleton(
    #     DtoContainer,
    # )

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
