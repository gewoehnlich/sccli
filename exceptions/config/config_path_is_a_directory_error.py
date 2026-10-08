from pathlib import Path
from exceptions.config.config_error import ConfigError


class ConfigPathIsADirectoryError(ConfigError):
    def __init__(
        self,
        path: Path,
    ) -> None:
        self.message = f"Config path is a directory: {path}"
