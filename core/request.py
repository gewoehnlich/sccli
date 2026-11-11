from typing import Any

from yarl import URL  # installed together with aiohttp

from domain.enums.http_method_enum import HttpMethodEnum
from exceptions.soundcloud_errors import (
    BuildUrlError,
    UnsupportedApiEndpointException,
)


class HttpMethods:
    GET: HttpMethodEnum = HttpMethodEnum.GET
    POST: HttpMethodEnum = HttpMethodEnum.POST
    PUT: HttpMethodEnum = HttpMethodEnum.PUT
    DELETE: HttpMethodEnum = HttpMethodEnum.DELETE


class Urls:
    AUTHORIZATION = "https://secure.soundcloud.com/authorize"
    TOKEN = "https://secure.soundcloud.com/oauth/token"
    REFRESH_TOKEN = "https://secure.soundcloud.com/oauth/token"
    API = "https://api.soundcloud.com"
    SNDCDN = "https://i1.sndcdn.com"


class Request:
    METHOD: HttpMethods = HttpMethods()

    URL: Urls = Urls()

    def __init__(
        self,
        method: HttpMethodEnum,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, Any] | None = None,
        access_token: str | None = None,
    ) -> None:
        if not any(
            url.startswith(api_endpoint)
            for api_endpoint in (
                self.URL.AUTHORIZATION,
                self.URL.TOKEN,
                self.URL.REFRESH_TOKEN,
                self.URL.API,
                self.URL.SNDCDN,
            )
        ):
            raise UnsupportedApiEndpointException(
                f"Unsupported API endpoint: {url}"
            )

        self.method: HttpMethodEnum = method
        self.url: str = url

        values = self._stringify(data or {})

        if method in (self.METHOD.GET, self.METHOD.DELETE):
            self.params: dict[str, str] = values
            self.data: dict[str, str] = {}
        else:
            self.params = {}
            self.data = values

        self.headers: dict[str, str] = dict(headers or {})
        self.headers.setdefault("Accept", "application/json; charset=utf-8")
        self.headers.setdefault(
            "Content-Type", "application/x-www-form-urlencoded"
        )

        if access_token and not self.is_image:
            self.headers["Authorization"] = f"OAuth {access_token}"

    @property
    def is_image(self) -> bool:
        return self.url.startswith(self.URL.SNDCDN)

    def build_url(self) -> str:
        try:
            return str(URL(self.url).update_query(self.params))
        except (TypeError, ValueError) as e:
            raise BuildUrlError("Could not build the URL") from e

    @staticmethod
    def _stringify(values: dict[str, Any]) -> dict[str, str]:
        return {
            key: (
                "true"
                if value is True
                else "false"
                if value is False
                else str(value)
            )
            for key, value in values.items()
            if value is not None
        }
