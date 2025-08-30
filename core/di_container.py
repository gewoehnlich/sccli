from dependency_injector import containers, providers
from di.actions_container import ActionsContainer
from di.auth_container import AuthContainer
from di.commands_container import CommandsContainer
from di.database_container import DatabaseContainer
from di.query_builder_container import QueryBuilderContainer
from di.requests_container import RequestsContainer
from di.tables_container import TablesContainer

class DiContainer(containers.DeclarativeContainer):
    config   = providers.Configuration()
    auth     = providers.Singleton(AuthContainer)
    db       = providers.Singleton(DatabaseContainer)
    query    = providers.Singleton(QueryBuilderContainer)
    actions  = providers.Singleton(ActionsContainer)
    commands = providers.Singleton(CommandsContainer)
    requests = providers.Singleton(RequestsContainer)
    tables   = providers.Singleton(TablesContainer)

    _instance = None

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        query_builder: QueryBuilder = self.query().query_builder

        db: Connection = Database(
            query_builder = query_builder
        )
        cursor: Cursor = db.cursor

        db.create_table_if_not_exists(
            table = TracksTable(
                cursor = cursor,
                query_builder = query_builder,
            )
        )

        db.create_table_if_not_exists(
            table = UsersTable(
                cursor = cursor,
                query_builder = query_builder,
            )
        )
