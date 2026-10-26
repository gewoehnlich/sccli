from exceptions.config.server.server_config_error import ServerConfigError


class RedirectUriInvalidHostError(ServerConfigError):
    def __init__(
        self,
        host: str | None,
    ) -> None:
        self.message = (
            f"Redirect URI host must be localhost or 127.0.0.1, got: {host}"
        )
