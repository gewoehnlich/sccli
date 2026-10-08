import errno
from pathlib import Path

import pytest

from core.config import Config
from core.config_loader import ConfigLoader
from exceptions.config.cannot_read_config_file_error import CannotReadConfigFileError
from exceptions.config.client_id_invalid_format_error import ClientIdInvalidFormatError
from exceptions.config.client_id_is_not_set_error import ClientIdIsNotSetError
from exceptions.config.client_secret_invalid_format_error import (
    ClientSecretInvalidFormatError,
)
from exceptions.config.client_secret_is_not_set_error import ClientSecretIsNotSetError
from exceptions.config.config_error import ConfigError
from exceptions.config.config_file_is_empty_error import ConfigFileIsEmptyError
from exceptions.config.config_file_must_be_utf_8_encoded_error import (
    ConfigFileMustBeUtf8EncodedError,
)
from exceptions.config.config_file_not_found_error import ConfigFileNotFoundError
from exceptions.config.config_path_is_a_directory_error import (
    ConfigPathIsADirectoryError,
)
from exceptions.config.invalid_yaml_config_error import InvalidYamlConfigError
from exceptions.config.no_permission_to_read_config_error import (
    NoPermissionToReadConfigError,
)


def test_config_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(ConfigFileNotFoundError):
        ConfigLoader().load(path=tmp_path / "missing.yml")


def test_config_path_is_a_directory(tmp_path: Path) -> None:
    with pytest.raises(ConfigPathIsADirectoryError):
        ConfigLoader().load(path=tmp_path)


def test_config_not_utf8(tmp_path: Path) -> None:
    path = tmp_path / "config.yml"
    path.write_bytes(b"\xff\xfe\x00")

    with pytest.raises(ConfigFileMustBeUtf8EncodedError):
        ConfigLoader().load(path=path)


def test_config_no_permission(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_permission_error(self: Path, *args: object, **kwargs: object):
        raise PermissionError(errno.EACCES, "Permission denied", str(self))

    monkeypatch.setattr(Path, "open", raise_permission_error)

    with pytest.raises(NoPermissionToReadConfigError):
        ConfigLoader().load(path=tmp_path / "config.yml")


def test_config_cannot_read_generic_os_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_os_error(self: Path, *args: object, **kwargs: object):
        raise OSError(errno.EIO, "Input/output error", str(self))

    monkeypatch.setattr(Path, "open", raise_os_error)

    with pytest.raises(CannotReadConfigFileError):
        ConfigLoader().load(path=tmp_path / "config.yml")


@pytest.mark.parametrize(
    "content",
    [
        "",  # truly empty
        "   \n\n",  # whitespace only
        "# just a comment\n",  # comments only
        "null\n",  # explicit null
        "~\n",  # YAML null shorthand
    ],
)
def test_config_file_is_empty(
    tmp_path: Path,
    content: str,
) -> None:
    path = tmp_path / "config.yml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ConfigFileIsEmptyError):
        ConfigLoader().load(path=path)


@pytest.mark.parametrize(
    "content",
    [
        "key: [unclosed",  # unterminated flow sequence
        "key: value\n  bad_indent: 1\n",  # invalid indentation
        "a: b: c\n",  # nested mapping on one line
        "!!python/object:os.system {}\n",  # unsafe tag rejected by safe_load
    ],
)
def test_config_invalid_yaml(
    tmp_path: Path,
    content: str,
) -> None:
    path = tmp_path / "config.yml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(InvalidYamlConfigError):
        ConfigLoader().load(path=path)


@pytest.mark.parametrize(
    ("content"),
    [
        ("- a\n- b\n"),
        ("just a string\n"),
        ("42\n"),
        ("true\n"),
    ],
)
def test_config_must_be_a_mapping(
    tmp_path: Path,
    content: str,
) -> None:
    path = tmp_path / "config.yml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ConfigError):
        ConfigLoader().load(path=path)


INVALID_FORMAT_SOUNDCLOUD_CREDENTIAL: str = "asdf"
VALID_FORMAT_SOUNDCLOUD_CREDENTIAL: str = "asdf1234asdf1234asdf1234asdf1234"


@pytest.mark.parametrize(
    ("content"),
    [
        (
            "soundcloud:\n"
            "  client_id:\n"
            "  client_secret: " + f"{VALID_FORMAT_SOUNDCLOUD_CREDENTIAL}\n"
            "proxy:\n"
            "  endpoint:\n"
        ),
    ],
)
def test_config_client_id_is_none(
    tmp_path: Path,
    content: str,
) -> None:
    path = tmp_path / "config.yml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ClientIdIsNotSetError):
        ConfigLoader().load(path=path)


@pytest.mark.parametrize(
    ("content"),
    [
        (
            "soundcloud:\n"
            "  client_id: " + f"{INVALID_FORMAT_SOUNDCLOUD_CREDENTIAL}\n"
            "  client_secret: " + f"{VALID_FORMAT_SOUNDCLOUD_CREDENTIAL}\n"
            "proxy:\n"
            "  endpoint:\n"
        ),
    ],
)
def test_invalid_format_config_client_id(
    tmp_path: Path,
    content: str,
) -> None:
    path = tmp_path / "config.yml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ClientIdInvalidFormatError):
        ConfigLoader().load(path=path)


@pytest.mark.parametrize(
    ("content"),
    [
        (
            "soundcloud:\n"
            "  client_id: " + f"{VALID_FORMAT_SOUNDCLOUD_CREDENTIAL}\n"
            "  client_secret:\n"
            "proxy:\n"
            "  endpoint:\n"
        ),
    ],
)
def test_config_client_secret_is_none(
    tmp_path: Path,
    content: str,
) -> None:
    path = tmp_path / "config.yml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ClientSecretIsNotSetError):
        ConfigLoader().load(path=path)


@pytest.mark.parametrize(
    ("content"),
    [
        (
            "soundcloud:\n"
            "  client_id: " + f"{VALID_FORMAT_SOUNDCLOUD_CREDENTIAL}\n"
            "  client_secret: " + f"{INVALID_FORMAT_SOUNDCLOUD_CREDENTIAL}\n"
            "proxy:\n"
            "  endpoint:\n"
        ),
    ],
)
def test_invalid_format_config_client_secret(
    tmp_path: Path,
    content: str,
) -> None:
    path = tmp_path / "config.yml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(ClientSecretInvalidFormatError):
        ConfigLoader().load(path=path)
