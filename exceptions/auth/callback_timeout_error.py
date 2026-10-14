from exceptions.auth.auth_error import AuthError


class CallbackTimeoutError(AuthError):
    message = "Callback timeout error!"
