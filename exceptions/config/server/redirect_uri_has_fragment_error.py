from exceptions.config.server.server_config_error import ServerConfigError


class RedirectUriHasFragmentError(ServerConfigError):
    def __init__(
        self,
        fragment: str,
    ) -> None:
        self.message = (
            f"Redirect URI must not contain a fragment string: {fragment}"
        )
