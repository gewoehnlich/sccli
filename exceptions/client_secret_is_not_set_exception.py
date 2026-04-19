class ClientSecretIsNotSetException(
    Exception
):
    def __init__(
        self,
    ):
        self.message = "client_secret has to be set in config.yml"
