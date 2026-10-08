from pathlib import Path

from pydantic import Field, ValidationError
from rich import inspect

from config.base_config_model import BaseConfigModel
from config.database import DatabaseConfig
from config.logs import LogsConfig
from config.messages import MessagesConfig
from config.proxy import ProxyConfig
from config.server import ServerConfig
from config.soundcloud import SoundcloudConfig
from config.tests import TestsConfig
from exceptions.config.client_id_invalid_format_error import ClientIdInvalidFormatError
from exceptions.config.client_id_is_not_set_error import ClientIdIsNotSetError
from exceptions.config.client_secret_invalid_format_error import (
    ClientSecretInvalidFormatError,
)
from exceptions.config.client_secret_is_not_set_error import ClientSecretIsNotSetError


type ConfigFileData = dict[str, str | None]


class Config(BaseConfigModel):
    soundcloud: SoundcloudConfig
    messages: MessagesConfig = Field(default_factory=MessagesConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    proxy: ProxyConfig = Field(default_factory=ProxyConfig)
    tests: TestsConfig = Field(default_factory=TestsConfig)
    logs: LogsConfig = Field(default_factory=LogsConfig)

    @classmethod
    def from_config_file_data(
        cls,
        config_file_data: ConfigFileData,
        path: Path,
    ) -> Config:
        try:
            return cls.model_validate(config_file_data)
        except ValidationError as e:
            for error in e.errors():
                if error["loc"] == ("soundcloud", "client_id"):
                    if error["input"] is None:
                        raise ClientIdIsNotSetError(config_file=path) from e
                    else:
                        raise ClientIdInvalidFormatError(config_file=path) from e
                if error["loc"] == ("soundcloud", "client_secret"):
                    if error["input"] is None:
                        raise ClientSecretIsNotSetError(config_file=path) from e
                    else:
                        raise ClientSecretInvalidFormatError(config_file=path) from e

            raise e
