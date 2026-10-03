from pathlib import Path
from exceptions.config.config_error import ConfigError


class ConfigFileMustBeUtf8EncodedError(ConfigError):
    def __init__(
        self,
        path: Path,
    ) -> None:
        self.message = f"{self.ERROR_MESSAGE_PREFIX} - Config file must be UTF-8 encoded: {path}"
