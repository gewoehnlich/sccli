from exceptions.config.config_error import ConfigError


class ServerConfigError(ConfigError):
    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message
