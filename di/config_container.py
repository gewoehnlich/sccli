from dependency_injector import containers, providers


class ConfigContainer(
    containers.DeclarativeContainer
):
    config = providers.Configuration()
