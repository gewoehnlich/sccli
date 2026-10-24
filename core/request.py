from typing import Any, cast

import requests
from requests import Request as BaseRequest, Response

from domain.enums.http_method_enum import HttpMethodEnum
from exceptions.soundcloud_errors import *


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
    _session = requests.Session()
    _session.proxies.update({
        "http": "http://172.17.0.1:52048",
        "https": "http://172.17.0.1:52048",
    })

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

        self._request = BaseRequest(
            method=method.value,
            url=url,
            headers=headers,
            params=params,
            data=data,
        )

    def send(
        self,
    ) -> dict[str, Any]:
        prepared: requests.PreparedRequest = self._session.prepare_request(
            request=self._request,
        )

        try:
            response: Response = self._session.send(
                request=prepared,
            )
        except requests.RequestException as e:
            raise SoundcloudConnectionError(
                f"Could not reach SoundCloud: {type(e).__name__})"
            ) from e

        if response.ok:
            return self._parse_body(response=response)

        error = self._build_error(response=response)

        raise error

    def build_url(
        self,
    ) -> str:
        url = self._request.prepare().url

        if url is None:
            raise BuildUrlError("Could not build the URL")

        return url

    @staticmethod
    def _parse_body(
        response: Response,
    ) -> dict[str, Any]:
        if response.status_code == 204 or not response.content:
            return {}

        try:
            data: Any = response.json()
        except ValueError as e:
            raise InvalidResponseError(
                "SoundCloud returned a non-JSON response"
            ) from e

        if not isinstance(data, dict):
            raise InvalidResponseError(
                f"Expected a JSON object, got {type(data).__name__}"
            )

        return cast("dict[str, Any]", data)

    def _build_error(
        self,
        response: Response,
    ) -> ApiError:
        body = self._parse_body(response=response)

        message = str(body.get("message"))

        status = response.status_code

        oauth_errors: dict[str, type[ApiError]] = {
            "invalid_grant": InvalidGrantError,
            "unsupported_grant": UnsupportedGrantError,
            "unsupported_grant_type": UnsupportedGrantError,
            "invalid_client": InvalidClientError,
            "invalid_scope": InvalidScopeError,
            "unauthorized_client": UnauthorizedClientError,
        }

        if status in (400, 401) and message in oauth_errors:
            return oauth_errors[message](status, message)

        if status == 429:
            spam_warning_urn = body.get("spam_warning_urn")

            return TooManyRequestsError(
                status=status,
                message=message,
                spam_warning_urn=spam_warning_urn,
            )

        status_errors: dict[int, type[ApiError]] = {
            400: BadRequestError,
            401: UnauthorizedError,
            403: ForbiddenError,
            404: NotFoundError,
            406: NotAcceptableError,
            422: UnprocessableEntityError,
            504: GatewayTimeoutError,
        }
        error_class = status_errors.get(status) or (
            ServerError if status >= 500 else ApiError
        )

        return error_class(status, message)
