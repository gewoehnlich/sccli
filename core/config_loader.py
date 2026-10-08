from pathlib import Path
from typing import Any, cast

import yaml

from core.config import Config
from exceptions.config.cannot_read_config_file_error import CannotReadConfigFileError
from exceptions.config.config_file_is_empty_error import ConfigFileIsEmptyError
from exceptions.config.config_file_must_be_utf_8_encoded_error import (
    ConfigFileMustBeUtf8EncodedError,
)
from exceptions.config.config_file_not_found_error import ConfigFileNotFoundError
from exceptions.config.config_path_is_a_directory_error import (
    ConfigPathIsADirectoryError,
)
from exceptions.config.invalid_yaml_config_error import InvalidYamlConfigError
from exceptions.config.invalid_config_file_format_error import (
    InvalidConfigFileFormatError,
)
from exceptions.config.no_permission_to_read_config_error import (
    NoPermissionToReadConfigError,
)


type ConfigFileData = dict[str, str | None]


class ConfigLoader:
    def load(
        self,
        path: Path,
    ) -> Config:
        try:
            with path.open(mode="r", encoding="utf-8") as f:
                data: Any = yaml.safe_load(f)
        except FileNotFoundError as e:
            raise ConfigFileNotFoundError(path=path) from e
        except IsADirectoryError as e:
            raise ConfigPathIsADirectoryError(path=path) from e
        except PermissionError as e:
            raise NoPermissionToReadConfigError(path=path) from e
        except OSError as e:
            raise CannotReadConfigFileError(path=path) from e
        except UnicodeDecodeError as e:
            raise ConfigFileMustBeUtf8EncodedError(path=path) from e
        except yaml.YAMLError as e:
            raise InvalidYamlConfigError(path=path) from e

        if data is None:
            raise ConfigFileIsEmptyError(path=path)

        if not isinstance(data, dict):
            raise InvalidConfigFileFormatError(datatype=type(data).__name__)

        config_file_data: ConfigFileData = cast("ConfigFileData", data)

        return Config.from_config_file_data(
            config_file_data=config_file_data,
            path=path,
        )
