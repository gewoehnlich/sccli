from pathlib import Path
import sys
from typing import Any

from rich import inspect
import yaml
from pydantic import ValidationError

from core.settings import Settings
from exceptions.config.config_error import ConfigError
from exceptions.config.cannot_read_config_file_error import CannotReadConfigFileError
from exceptions.config.config_file_is_empty_error import ConfigFileIsEmptyError
from exceptions.config.config_file_must_be_utf_8_encoded_error import ConfigFileMustBeUtf8EncodedError
from exceptions.config.config_file_not_found_error import ConfigFileNotFoundError
from exceptions.config.config_path_is_a_directory_error import ConfigPathIsADirectoryError
from exceptions.config.invalid_yaml_config_error import InvalidYamlConfigError
from exceptions.config.no_permission_to_read_config_error import NoPermissionToReadConfigError
from exceptions.client_id_is_not_set_exception import ClientIdIsNotSetException
from exceptions.client_secret_is_not_set_exception import ClientSecretIsNotSetException


class Config:
    DEFAULT_PATH: Path = Path("config.yml")

    def __init__(
        self,
        path: Path = DEFAULT_PATH,
    ) -> None:
        self._path = path

    def load(
        self,
    ) -> Settings:
        user_config_data: dict[str, Any] = self.__read_user_config_data()

        self.__ensure_client_credentials_are_set(
            config_data=user_config_data,
        )

        filtered_config: dict[str, Any] = self.__remove_none_values(
            config=user_config_data
        )

        settings: Settings = self.__add_default_values(config=filtered_config)

        return settings

    def __read_user_config_data(
        self,
    ) -> dict[str, Any]:
        try:
            with self._path.open(encoding="utf-8") as f:
                data: dict[str, Any] | None = yaml.safe_load(f)
        except FileNotFoundError as e:
            raise ConfigFileNotFoundError(path=self._path) from e
        except IsADirectoryError as e:
            raise ConfigPathIsADirectoryError(path=self._path) from e
        except PermissionError as e:
            raise NoPermissionToReadConfigError(path=self._path) from e
        except OSError as e:
            raise CannotReadConfigFileError(path=self._path) from e
        except UnicodeDecodeError as e:
            raise ConfigFileMustBeUtf8EncodedError(path=self._path) from e
        except yaml.YAMLError as e:
            raise InvalidYamlConfigError(path=self._path) from e

        if data is None:
            raise ConfigFileIsEmptyError(path=self._path)

        if not isinstance(data, dict):
            raise ConfigError(
                f"Config must be a mapping of keys to values, got {type(data).__name__}"
            )

        inspect(data);
        sys.exit(1)

        return data


    def __ensure_client_credentials_are_set(
        self,
        config_data: dict[str, Any],
    ) -> None:
        client_id = config_data["soundcloud"]["client_id"]
        if not isinstance(client_id, str) or not client_id:
            raise ClientIdIsNotSetException

        client_secret = config_data["soundcloud"]["client_secret"]
        if not isinstance(client_secret, str) or not client_secret:
            raise ClientSecretIsNotSetException

    def __remove_none_values(
        self,
        config: dict[str, Any],
    ) -> dict[str, Any]:
        if isinstance(config, dict):
            return {
                key: self.__remove_none_values(value)
                for key, value in config.items()
                if value is not None
            }

        return config

    def __add_default_values(
        self,
        config: dict[str, Any],
    ) -> Settings:
        try:
            settings = Settings.model_validate(config)
        except ValidationError as e:
            print(
                f"ERROR: Invalid configuration in '{self.CONFIG_PATH}':\n{e}",
                file=sys.stderr,
            )
            sys.exit(1)

        return settings
