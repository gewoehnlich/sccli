from exceptions.auth.auth_error import AuthError


class PortUnavailableError(AuthError):
    def __init__(
        self,
        port: int,
    ) -> None:
        self.message = f"Port unavailable error: {port}"
