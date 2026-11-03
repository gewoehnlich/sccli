from typing import Any, cast

import requests

from core.request import Request
from exceptions.soundcloud_errors import *


class HttpClient:
    _session = requests.Session()

    def __init__(
        self,
        proxy_endpoint: str | None = None,
    ) -> None:
        if proxy_endpoint:
            self._session.proxies.update(
                {
                    "http": proxy_endpoint,
                    "https": proxy_endpoint,
                }
            )

    def send(
        self,
        request: Request,
    ) -> dict[str, Any]:
        prepared: requests.PreparedRequest = self._session.prepare_request(
            request=request.base_request,
        )

        try:
            response: requests.Response = self._session.send(
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

    @staticmethod
    def _parse_body(
        response: requests.Response,
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
        response: requests.Response,
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
