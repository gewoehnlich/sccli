from exceptions.config.config_error import ConfigError


class InvalidConfigFileFormatError(ConfigError):
    def __init__(
        self,
        datatype: str,
    ) -> None:
        self.message = f"{self.ERROR_MESSAGE_PREFIX} - Config must be a mapping of keys to values, got {datatype}"
