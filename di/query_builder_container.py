from dependency_injector import containers, providers
from core.query_builder import QueryBuilder


class QueryBuilderContainer(containers.DeclarativeContainer):
    query_builder = providers.Singleton(QueryBuilder)
