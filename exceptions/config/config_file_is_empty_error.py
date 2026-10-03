from pathlib import Path
from exceptions.config.config_error import ConfigError


class ConfigFileIsEmptyError(ConfigError):
    def __init__(
        self,
        path: Path,
    ) -> None:
        self.message = f"{self.ERROR_MESSAGE_PREFIX} - Config file is empty: {path}"
