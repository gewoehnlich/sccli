from urllib.parse import urlsplit

from pydantic import field_validator

from config.base_config_model import BaseConfigModel
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


class ServerConfig(BaseConfigModel):
    redirect_uri: str = "http://localhost:16501/callback"

    @field_validator("redirect_uri")
    @classmethod
    def _redirect_uri(cls, value: str) -> str:
        parts = urlsplit(value)

        if parts.scheme != "http":
            raise RedirectUriNotHttpError(scheme=parts.scheme)
        if parts.hostname not in {"localhost", "127.0.0.1"}:
            raise RedirectUriInvalidHostError(host=parts.hostname)
        if parts.port is None:
            raise RedirectUriNoPortError(port=parts.port)
        if parts.path in {"", "/"}:
            raise RedirectUriNoCallbackPathError(path=parts.path)
        if parts.query:
            raise RedirectUriHasQueryError(query=parts.query)
        if parts.fragment:
            raise RedirectUriHasFragmentError(fragment=parts.fragment)

        return value

    @property
    def host(self) -> str:
        host = urlsplit(self.redirect_uri).hostname
        assert host is not None

        return host

    @property
    def port(self) -> int:
        port = urlsplit(self.redirect_uri).port
        assert port is not None

        return port

    @property
    def path(self) -> str:
        return urlsplit(self.redirect_uri).path
