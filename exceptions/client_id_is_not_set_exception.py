class ClientIdIsNotSetException(Exception):
    def __init__(
        self,
    ):
        self.message = "client_id has to be set in config.yml"
