from exceptions.servers.server_error import ServerError


class PortUnavailableError(ServerError):
    def __init__(
        self,
        port: int,
    ) -> None:
        self.message = f"Port unavailable error: {port}"
