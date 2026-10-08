from pathlib import Path

from exceptions.config.config_error import ConfigError


class ClientSecretInvalidFormatError(ConfigError):
    def __init__(
        self,
        config_file: Path,
    ) -> None:
        self.message = f"Invalid soundcloud.client_secret format in {config_file}"
