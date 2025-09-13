from dependency_injector import containers, providers

from requests_.authentication_request import AuthenticationRequest
from requests_.refresh_token_request import RefreshTokenRequest


class AuthRequestsContainer(containers.DeclarativeContainer):
    authentication = providers.Factory(AuthenticationRequest)
    refresh_token  = providers.Factory(RefreshTokenRequest)
