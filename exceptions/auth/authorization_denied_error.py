from exceptions.auth.auth_error import AuthError


class AuthorizationDeniedError(AuthError):
    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = f"Authorization denied error: {message}"
