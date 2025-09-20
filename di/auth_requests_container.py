from dependency_injector import containers, providers

from api_requests.authentication_request import AuthenticationRequest
from api_requests.refresh_token_request import RefreshTokenRequest


class AuthRequestsContainer(
    containers.DeclarativeContainer
):
    dto = providers.DependenciesContainer()

    authentication = providers.Factory(
        AuthenticationRequest,
        dto = dto.authentication,
    )
    refresh_token = providers.Factory(
        RefreshTokenRequest,
        dto = dto.refresh_token
    )
