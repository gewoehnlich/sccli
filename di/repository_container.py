from dependency_injector import containers, providers

from repositories.account_repository import AccountRepository


class RepositoryContainer(
    containers.DeclarativeContainer
):
    session_factory = providers.Dependency()

    account = providers.Singleton(
        AccountRepository,
        session_factory = session_factory,
    )
