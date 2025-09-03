from dependency_injector import containers, providers
from di.actions_container import ActionsContainer
from di.auth_container import AuthContainer
from di.commands_container import CommandsContainer
from di.database_container import DatabaseContainer
from di.query_builder_container import QueryBuilderContainer
from di.requests_container import RequestsContainer
from di.server_container import ServerContainer
from di.tables_container import TablesContainer
from utils.enums import DatabaseEnum


class DiContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    query_builder = providers.Singleton(QueryBuilderContainer)
    tables = providers.Singleton(TablesContainer)
    db = providers.Singleton(
        DatabaseContainer,
        db = DatabaseEnum.SQLITE.name,
        tables = tables,
        query_builder = query_builder,
    )

    auth = providers.Singleton(
        AuthContainer,
        client_id     = config.client_id,
        client_secret = config.client_secret,
        redirect_uri  = config.redirect_uri,
        tokens_file   = ".tokens.json",
    )

    server = providers.Singleton(
        ServerContainer,
        server_port = config.server_port,
        server_path = config.server_path,
    )

    actions  = providers.Singleton(ActionsContainer)
    commands = providers.Singleton(CommandsContainer)
    requests = providers.Singleton(RequestsContainer)

    _instance = None


    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def __init__(self) -> None:
        self.initialize_tables()


    def initialize_tables(self) -> None:
        db:     DatabaseContainer = self.db()
        tables: TablesContainer   = self.tables()

        db.create_table_if_not_exists(
            table = tables.tracks
        )

        db.create_table_if_not_exists(
            table = tables.users
        )
