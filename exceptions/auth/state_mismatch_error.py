from exceptions.auth.auth_error import AuthError


class StateMismatchError(AuthError):
    message = "State mismatch error!"
