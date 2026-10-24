from typing import Any, cast

import requests
from requests import Request as BaseRequest, Response

from domain.enums.soundcloud_api_endpoint_enum import SoundcloudApiEndpointEnum
from exceptions.soundcloud_errors import *


class Request:
    _session = requests.Session()

    AUTHORIZATION_API_ENDPOINT: str = (
        SoundcloudApiEndpointEnum.AUTHORIZATION.value
    )

    TOKEN_API_ENDPOINT: str = SoundcloudApiEndpointEnum.TOKEN.value

    REFRESH_TOKEN_API_ENDPOINT: str = (
        SoundcloudApiEndpointEnum.REFRESH_TOKEN.value
    )

    SOUNDCLOUD_API_ENDPOINT: str = SoundcloudApiEndpointEnum.API.value

    def __init__(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
        access_token: str | None = None,
    ) -> None:
        method = method.upper()

        if data is None:
            data = {}

        if params is None:
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
            method=method,
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
