from pathlib import Path
from exceptions.config.config_error import ConfigError


class InvalidYamlConfigError(ConfigError):
    def __init__(
        self,
        path: Path,
    ) -> None:
        self.message = f"{self.ERROR_MESSAGE_PREFIX} - Invalid yaml config: {path}"
