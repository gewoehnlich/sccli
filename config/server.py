from urllib.parse import urlsplit

from pydantic import field_validator

from config.base_config_model import BaseConfigModel
from exceptions.config.server_config_error import ServerConfigError


class ServerConfig(BaseConfigModel):
    redirect_uri: str = "http://localhost:16501/callback"

    @field_validator("redirect_uri")
    @classmethod
    def _redirect_uri(cls, value: str) -> str:
        parts = urlsplit(value)

        if parts.scheme != "http":
            raise ServerConfigError("must start with http://")
        if parts.hostname not in {"localhost", "127.0.0.1"}:
            raise ServerConfigError("host must be localhost or 127.0.0.1")
        if parts.port is None:
            raise ServerConfigError("must include a port, e.g. :16501")
        if parts.path in {"", "/"}:
            raise ServerConfigError("must include a callback path, e.g. /callback")
        if parts.query or parts.fragment:
            raise ServerConfigError("must not contain a query string or fragment")

        return value

    @property
    def host(self) -> str:
        host =  urlsplit(self.redirect_uri).hostname
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
