from exceptions.config.config_error import ConfigError


class InvalidConfigFileFormatError(ConfigError):
    def __init__(
        self,
        datatype: str,
    ) -> None:
        self.message = f"Config expected to be dict, got {datatype}"
