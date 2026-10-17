from exceptions.config.server.server_config_error import ServerConfigError


class RedirectUriNoPortError(ServerConfigError):
    def __init__(
        self,
        port: None,
    ) -> None:
        self.message = (
            f"Redirect URI must include a port, e.g. :16501, got: {port}"
        )
