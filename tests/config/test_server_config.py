from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from config.server import ServerConfig
from core.config_loader import ConfigLoader
from exceptions.config.server.redirect_uri_has_fragment_error import (
    RedirectUriHasFragmentError,
)
from exceptions.config.server.redirect_uri_has_query_error import (
    RedirectUriHasQueryError,
)
from exceptions.config.server.redirect_uri_invalid_host_error import (
    RedirectUriInvalidHostError,
)
from exceptions.config.server.redirect_uri_no_callback_path_error import (
    RedirectUriNoCallbackPathError,
)
from exceptions.config.server.redirect_uri_no_port_error import (
    RedirectUriNoPortError,
)
from exceptions.config.server.redirect_uri_not_http_error import (
    RedirectUriNotHttpError,
)

DEFAULT_URI = "http://localhost:16501/callback"


def rejection(
    uri: str,
) -> BaseException:
    """Return the custom error raised for `uri`, however pydantic delivers it."""
    try:
        ServerConfig(redirect_uri=uri)
    except ValidationError as e:
        error = e.errors()[0].get("ctx", {}).get("error")
        assert isinstance(error, BaseException), (
            f"unexpected validation error: {e}"
        )
        return error
    except Exception as e:
        return e

    raise AssertionError(f"{uri!r} was accepted")


def test_default_redirect_uri() -> None:
    config = ServerConfig()

    assert config.redirect_uri == DEFAULT_URI
    assert (config.host, config.port, config.path) == (
        "localhost",
        16501,
        "/callback",
    )


def test_default_passes_its_own_validator() -> None:
    ServerConfig(redirect_uri=ServerConfig().redirect_uri)


@pytest.mark.parametrize(
    ("uri", "host", "port", "path"),
    [
        (DEFAULT_URI, "localhost", 16501, "/callback"),
        ("http://127.0.0.1:9000/oauth/cb", "127.0.0.1", 9000, "/oauth/cb"),
        ("http://LocalHost:8080/callback/", "localhost", 8080, "/callback/"),
    ],
)
def test_properties_are_derived_from_the_uri(
    uri: str,
    host: str,
    port: int,
    path: str,
) -> None:
    config = ServerConfig(redirect_uri=uri)

    assert (config.host, config.port, config.path) == (host, port, path)


@pytest.mark.parametrize(
    "uri",
    [
        DEFAULT_URI,
        "http://localhost:8080/callback",
        "http://127.0.0.1:9000/callback",
        "http://localhost:16501/oauth/soundcloud/callback",
        "http://localhost:16501/callback/",
        "http://LocalHost:16501/callback",
        "HTTP://localhost:16501/callback",
        "http://localhost:1/callback",
        "http://localhost:65535/callback",
    ],
)
def test_valid_redirect_uri_is_accepted_unchanged(
    uri: str,
) -> None:
    assert ServerConfig(redirect_uri=uri).redirect_uri == uri


INVALID: list[tuple[str, type[Exception]]] = [
    # scheme
    ("https://localhost:16501/callback", RedirectUriNotHttpError),
    ("ftp://localhost:16501/callback", RedirectUriNotHttpError),
    ("my-app://soundcloud/callback", RedirectUriNotHttpError),
    ("localhost:16501/callback", RedirectUriNotHttpError),
    ("//localhost:16501/callback", RedirectUriNotHttpError),
    ("", RedirectUriNotHttpError),
    # host
    ("http://example.com:16501/callback", RedirectUriInvalidHostError),
    ("http://0.0.0.0:16501/callback", RedirectUriInvalidHostError),
    ("http://127.0.0.2:16501/callback", RedirectUriInvalidHostError),
    ("http://[::1]:16501/callback", RedirectUriInvalidHostError),
    ("http://localhost.evil.com:16501/callback", RedirectUriInvalidHostError),
    ("http://:16501/callback", RedirectUriInvalidHostError),
    ("http:///callback", RedirectUriInvalidHostError),
    # port
    ("http://localhost/callback", RedirectUriNoPortError),
    ("http://127.0.0.1/callback", RedirectUriNoPortError),
    ("http://localhost:/callback", RedirectUriNoPortError),
    # path
    ("http://localhost:16501", RedirectUriNoCallbackPathError),
    ("http://localhost:16501/", RedirectUriNoCallbackPathError),
    # query
    ("http://localhost:16501/callback?x=1", RedirectUriHasQueryError),
    ("http://localhost:16501/callback?x=1#section", RedirectUriHasQueryError),
    # fragment
    ("http://localhost:16501/callback#section", RedirectUriHasFragmentError),
]


@pytest.mark.parametrize(("uri", "expected"), INVALID)
def test_invalid_redirect_uri_raises_the_specific_error(
    uri: str,
    expected: type[Exception],
) -> None:
    assert type(rejection(uri)) is expected


@pytest.mark.parametrize(
    ("uri", "expected"),
    [
        ("https://example.com?x=1#f", RedirectUriNotHttpError),
        ("http://example.com?x=1#f", RedirectUriInvalidHostError),
        ("http://localhost?x=1#f", RedirectUriNoPortError),
        ("http://localhost:16501?x=1#f", RedirectUriNoCallbackPathError),
    ],
)
def test_rules_are_checked_in_order(
    uri: str,
    expected: type[Exception],
) -> None:
    assert type(rejection(uri)) is expected


def test_custom_errors_propagate_without_validation_error_wrapping() -> None:
    with pytest.raises(RedirectUriNotHttpError):
        ServerConfig(redirect_uri="https://localhost:16501/callback")


@pytest.mark.parametrize(
    "uri",
    [
        "http://localhost:99999/callback",
        "http://localhost:65536/callback",
        "http://localhost:abc/callback",
        "http://localhost:-1/callback",
    ],
)
def test_unparseable_port_is_a_plain_validation_error(
    uri: str,
) -> None:
    with pytest.raises(ValidationError):
        ServerConfig(redirect_uri=uri)


def test_unknown_keys_are_rejected() -> None:
    with pytest.raises(ValidationError):
        ServerConfig.model_validate({"redirect_uri": DEFAULT_URI, "port": 8080})


def test_model_is_frozen() -> None:
    config = ServerConfig()

    with pytest.raises(ValidationError):
        config.redirect_uri = "http://localhost:1/callback"


def write_config(
    tmp_path: Path,
    server: object = None,
) -> Path:
    data: dict[str, object] = {
        "soundcloud": {
            "client_id": "a1b2c3d4" * 4,
            "client_secret": "e5f6a7b8" * 4,
        },
    }
    if server is not None:
        data["server"] = server

    path = tmp_path / "config.yml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")

    return path


def test_loader_reads_a_custom_redirect_uri(
    tmp_path: Path,
) -> None:
    path = write_config(tmp_path, {"redirect_uri": "http://127.0.0.1:9000/cb"})

    config = ConfigLoader().load(path=path)

    assert config.server.redirect_uri == "http://127.0.0.1:9000/cb"
    assert (config.server.host, config.server.port, config.server.path) == (
        "127.0.0.1",
        9000,
        "/cb",
    )


def test_loader_uses_the_default_without_a_server_section(
    tmp_path: Path,
) -> None:
    config = ConfigLoader().load(path=write_config(tmp_path))

    assert config.server.redirect_uri == DEFAULT_URI


def test_loader_surfaces_the_specific_redirect_uri_error(
    tmp_path: Path,
) -> None:
    path = write_config(
        tmp_path, {"redirect_uri": "https://localhost:16501/callback"}
    )

    with pytest.raises(RedirectUriNotHttpError):
        ConfigLoader().load(path=path)
