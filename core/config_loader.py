from pathlib import Path
import sys
from typing import Any, cast

from rich import inspect
import yaml
from pydantic import ValidationError

from core.config import Config
from exceptions.config.cannot_read_config_file_error import CannotReadConfigFileError
from exceptions.config.config_file_is_empty_error import ConfigFileIsEmptyError
from exceptions.config.config_file_must_be_utf_8_encoded_error import ConfigFileMustBeUtf8EncodedError
from exceptions.config.config_file_not_found_error import ConfigFileNotFoundError
from exceptions.config.config_path_is_a_directory_error import ConfigPathIsADirectoryError
from exceptions.config.invalid_yaml_config_error import InvalidYamlConfigError
from exceptions.config.invalid_config_file_format_error import InvalidConfigFileFormatError
from exceptions.config.no_permission_to_read_config_error import NoPermissionToReadConfigError
from exceptions.config.client_id_is_not_set_exception import ClientIdIsNotSetException
from exceptions.config.client_secret_is_not_set_exception import ClientSecretIsNotSetException


type ConfigFileData = dict[str, Any]

class ConfigLoader:
    def __init__(
        self,
        path: Path,
    ) -> None:
        self._path: Path = path

    def load(
        self,
    ) -> Config:
        user_config_data: ConfigFileData = self._read_user_config_data()

        filtered_config: ConfigFileData = cast(
            "ConfigFileData",
            self._remove_none_values(
                value=user_config_data,
            ),
        )

        config: Config = self._validate(
            data=filtered_config,
        )

        return config

    def _read_user_config_data(
        self,
    ) -> ConfigFileData:
        try:
            with self._path.open(encoding="utf-8") as f:
                data: Any = yaml.safe_load(f)
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
            raise InvalidConfigFileFormatError(datatype=type(data).__name__)

        return cast("ConfigFileData", data)


    def _remove_none_values(
        self,
        value: object,
    ) -> object:
        if isinstance(value, dict):
            mapping = cast("ConfigFileData", value)

            return {
                key: self._remove_none_values(item)
                for key, item in mapping.items()
                if item is not None
            }

        return value

    def _validate(
        self,
        data: ConfigFileData,
    ) -> Config:
        try:
            return Config.model_validate(data)
        except ValidationError as e:
            raise ValidationError from e
