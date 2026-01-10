from core.dto import Dto


class TokensDto(
    Dto
):
    client_id:        str
    client_secret:    str
    access_token:     str
    refresh_token:    str
    expire_timestamp: int
