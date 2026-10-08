from pathlib import Path

from exceptions.config.config_error import ConfigError


class ClientIdInvalidFormatError(ConfigError):
    def __init__(
        self,
        config_file: Path,
    ) -> None:
        self.message = f"Invalid soundcloud.client_id format in {config_file}"
