from pathlib import Path
from exceptions.config.config_error import ConfigError


class CannotReadConfigFileError(ConfigError):
    def __init__(
        self,
        path: Path,
    ) -> None:
        self.message = f"{self.ERROR_MESSAGE_PREFIX} - Cannot read config: {path}"
