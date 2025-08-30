from dependency_injector import containers, providers
from core.auth import Auth


class AuthContainer(containers.DeclarativeContainer):
    auth = providers.Singleton(Auth)
