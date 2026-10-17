from exceptions.config.server.server_config_error import ServerConfigError


class RedirectUriHasQueryError(ServerConfigError):
    def __init__(
        self,
        query: str,
    ) -> None:
        self.message = f"Redirect URI must not contain a query string: {query}"
