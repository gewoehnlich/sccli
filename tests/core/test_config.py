import pytest

from pathlib import Path
from core.config import Config
from exceptions.config.config_error import ConfigError
from exceptions.config.cannot_read_config_file_error import CannotReadConfigFileError
from exceptions.config.config_file_is_empty_error import ConfigFileIsEmptyError
from exceptions.config.config_file_must_be_utf_8_encoded_error import ConfigFileMustBeUtf8EncodedError
from exceptions.config.config_file_not_found_error import ConfigFileNotFoundError
from exceptions.config.config_path_is_a_directory_error import ConfigPathIsADirectoryError
from exceptions.config.invalid_yaml_config_error import InvalidYamlConfigError
from exceptions.config.no_permission_to_read_config_error import NoPermissionToReadConfigError


def test_config_file_not_found(tmp_path: Path) -> None:
    config = Config(path=tmp_path / "missing.yml")

    with pytest.raises(ConfigFileNotFoundError):
        config.load()


def test_config_path_is_a_directory(tmp_path: Path) -> None:
    config = Config(path=tmp_path)  # tmp_path is a directory

    with pytest.raises(ConfigPathIsADirectoryError):
        config.load()


def test_config_not_utf8(tmp_path: Path) -> None:
    path = tmp_path / "config.yml"
    path.write_bytes(b"\xff\xfe\x00")

    with pytest.raises(ConfigFileMustBeUtf8EncodedError):
        Config(path=path).load()
