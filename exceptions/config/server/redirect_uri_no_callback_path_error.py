from exceptions.config.server.server_config_error import ServerConfigError


class RedirectUriNoCallbackPathError(ServerConfigError):
    def __init__(
        self,
        path: str,
    ) -> None:
        self.message = f"Redirect URI must include a callback path, e.g. /callback, got: {path}"
