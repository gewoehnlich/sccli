from pathlib import Path
from exceptions.config.config_error import ConfigError


class NoPermissionToReadConfigError(ConfigError):
    def __init__(
        self,
        path: Path,
    ) -> None:
        self.message = f"No permission to read config: {path}"
