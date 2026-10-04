from pathlib import Path

from exceptions.config.config_error import ConfigError


class ClientIdIsNotSetException(ConfigError):
    def __init__(
        self,
        config_file: Path,
    ) -> None:
        self.message = f"{self.ERROR_MESSAGE_PREFIX} - client_id has to be set in {config_file}"
