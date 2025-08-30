from dependency_injector import containers, providers
from core.database import Database
from core.query_builder import QueryBuilder
from di.actions_container import ActionsContainer
from di.commands_container import CommandsContainer
from di.requests_container import RequestsContainer
from di.tables_container import TablesContainer

class DiContainer(containers.DeclarativeContainer):
    config   = providers.Configuration()
    db       = providers.Singleton(Database)
    query    = providers.Factory(QueryBuilder)
    actions  = providers.Factory(ActionsContainer)
    commands = providers.Factory(CommandsContainer)
    requests = providers.Factory(RequestsContainer)
    tables   = providers.Factory(TablesContainer)
