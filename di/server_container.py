from dependency_injector import containers, providers
from core.server import Server


class ServerContainer(containers.DeclarativeContainer):
    server = providers.Singleton(Server)
