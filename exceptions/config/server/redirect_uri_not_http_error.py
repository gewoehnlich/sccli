from exceptions.config.server.server_config_error import ServerConfigError


class RedirectUriNotHttpError(ServerConfigError):
    def __init__(
        self,
        scheme: str,
    ) -> None:
        self.message = f"Redirect URI must start with http://, got: {scheme}"
