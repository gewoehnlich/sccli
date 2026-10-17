from exceptions.servers.server_error import ServerError


class CallbackTimeoutError(ServerError):
    message = "Callback timeout error!"
