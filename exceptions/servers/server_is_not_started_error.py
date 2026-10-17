from exceptions.servers.server_error import ServerError


class ServerIsNotStartedError(ServerError):
    message = "Server is not started!"
