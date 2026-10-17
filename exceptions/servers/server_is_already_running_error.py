from exceptions.servers.server_error import ServerError


class ServerIsAlreadyRunningError(ServerError):
    message = "Server is already running!"
