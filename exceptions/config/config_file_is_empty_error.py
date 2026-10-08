from pathlib import Path
from exceptions.config.config_error import ConfigError


class ConfigFileIsEmptyError(ConfigError):
    def __init__(
        self,
        path: Path,
    ) -> None:
        self.message = f"Config file is empty: {path}"
