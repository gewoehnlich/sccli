from dependency_injector import containers, providers

from dto.authentication_dto import AuthenticationDto
from dto.refresh_token_dto  import RefreshTokenDto
from dto.tokens_dto         import TokensDto
from dto.track_dto          import TrackDto
from dto.user_dto           import UserDto


class DtoContainer(
    containers.DeclarativeContainer
):
    tokens = providers.Object(
        TokensDto,
    )
    track = providers.Object(
        TrackDto,
    )
    user = providers.Object(
        UserDto,
    )
    authentication = providers.Object(
        AuthenticationDto,
    )
    refresh_token = providers.Object(
        RefreshTokenDto,
    )
