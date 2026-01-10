from dependency_injector import containers, providers

from repositories.account_repository import AccountRepository


class RepositoryContainer(
    containers.DeclarativeContainer
):
    database = providers.Dependency()

    account = providers.Singleton(
        AccountRepository,
        database = database,
    )
