from typing import Any

from requests import Request as BaseRequest

from domain.enums.http_method_enum import HttpMethodEnum
from exceptions.soundcloud_errors import BuildUrlError, UnsupportedApiEndpointException


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
            )
        ):
            raise UnsupportedApiEndpointException(
                f"Unsupported API endpoint: {url}"
            )

        if data is None:
            params = {}
            data = {}
        elif method in (self.METHOD.GET, self.METHOD.DELETE):
            params = data
            data = {}
        else:
            params = {}

        if headers is None:
            headers = {}

        if headers.get("Accept") is None:
            headers["Accept"] = "application/json; charset=utf-8"

        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        if access_token:
            headers["Authorization"] = f"OAuth {access_token}"

        self.base_request = BaseRequest(
            method=method.value,
            url=url,
            headers=headers,
            params=params,
            data=data,
        )

    def build_url(
        self,
    ) -> str:
        url = self.base_request.prepare().url

        if url is None:
            raise BuildUrlError("Could not build the URL")

        return url
