from datetime import UTC, datetime
import time
from typing import Any, cast

import requests
from requests import Request as BaseRequest, Response

from domain.enums.soundcloud_api_endpoint_enum import SoundcloudApiEndpointEnum
from exceptions.soundcloud_errors import *

_OAUTH_ERRORS: dict[str, type[ApiError]] = {
    "invalid_grant": InvalidGrantError,
    "unsupported_grant": UnsupportedGrantError,
    "unsupported_grant_type": UnsupportedGrantError,
    "invalid_client": InvalidClientError,
    "invalid_scope": InvalidScopeError,
    "unauthorized_client": UnauthorizedClientError,
}

_STATUS_ERRORS: dict[int, type[ApiError]] = {
    400: BadRequestError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    406: NotAcceptableError,
    422: UnprocessableEntityError,
    504: GatewayTimeoutError,
}


def _clean(
    text: str,
) -> str:
    """One printable line, short enough for a log: no escape sequences, no newlines."""
    return "".join(c if c.isprintable() else " " for c in text).strip()[:200]


class Request:
    _session = requests.Session()

    AUTHORIZATION_API_ENDPOINT: str = (
        SoundcloudApiEndpointEnum.AUTHORIZATION.value
    )
    TOKEN_API_ENDPOINT: str = (
        SoundcloudApiEndpointEnum.TOKEN.value
    )
    REFRESH_TOKEN_API_ENDPOINT: str = (
        SoundcloudApiEndpointEnum.REFRESH_TOKEN.value
    )
    SOUNDCLOUD_API_ENDPOINT: str = (
        SoundcloudApiEndpointEnum.API.value
    )

    TIMEOUT: tuple[float, float] = (3.05, 15.0)
    MAX_RETRIES: int = 2
    MAX_AUTO_WAIT: float = 10.0
    IDEMPOTENT_METHODS = frozenset({"GET", "HEAD"})
    RETRYABLE_STATUSES = frozenset({429, 500, 502, 503, 504})

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

        attempt: int = 0

        while True:
            attempt += 1

            try:
                response: Response = self._session.send(
                    request=prepared,
                    timeout=self.TIMEOUT,
                )
            except requests.RequestException as e:
                if (
                    isinstance(e, (requests.ConnectionError, requests.Timeout))
                    and self._retryable(attempt=attempt)
                ):
                    time.sleep(self._time_to_wait(attempt=attempt))
                    continue

                raise SoundcloudConnectionError(
                    f"Could not reach SoundCloud ({type(e).__name__})"
                ) from e

            if response.ok:
                return self._parse_body(response)

            error = self._build_error(response)

            if (
                self._retryable(attempt=attempt)
                and response.status_code in self.RETRYABLE_STATUSES
            ):
                delay = self._delay(error, attempt)

                if delay is not None:
                    time.sleep(delay)
                    continue

            raise error

    def _retryable(
        self,
        attempt: int,
    ) -> bool:
        return (
            self._request.method in self.IDEMPOTENT_METHODS
            and attempt <= self.MAX_RETRIES
        )

    def _time_to_wait(
        self,
        attempt: int,
    ) -> float:
        return min(2 * 2 ** (attempt - 1), self.MAX_AUTO_WAIT)

    def _delay(
        self,
        error: ApiError,
        attempt: int,
    ) -> float | None:
        if (
            isinstance(error, TooManyRequestsError)
            and error.retry_after is not None
        ):
            return (
                error.retry_after
                if error.retry_after <= self.MAX_AUTO_WAIT
                else None
            )

        return self._time_to_wait(attempt)

    @staticmethod
    def _parse_body(
        response: Response,
    ) -> dict[str, Any]:
        if response.status_code == 204 or not response.content:
            return {}

        try:
            data: object = response.json()
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
        status = response.status_code
        body = self._json_object(response)
        message = _clean(self._message(body) or response.reason or "no details")

        if status in (400, 401) and message in _OAUTH_ERRORS:
            return _OAUTH_ERRORS[message](status, message)

        if status == 429:
            urn = body.get("spam_warning_urn") if body else None

            return TooManyRequestsError(
                status,
                message,
                retry_after=self._retry_after(response, body),
                spam_warning_urn=urn if isinstance(urn, str) else None,
            )

        error_class = _STATUS_ERRORS.get(status) or (
            ServerError if status >= 500 else ApiError
        )

        return error_class(status, message)

    @staticmethod
    def _json_object(
        response: Response,
    ) -> dict[str, Any] | None:
        try:
            data: object = response.json()
        except ValueError:
            return None

        return cast("dict[str, Any]", data) if isinstance(data, dict) else None

    @staticmethod
    def _message(
        body: dict[str, Any] | None,
    ) -> str | None:
        if body is None:
            return None

        for key in ("message", "error"):
            value = body.get(key)
            if isinstance(value, str) and value:
                return value

        errors = body.get("errors")
        if isinstance(errors, list):
            for item in cast("list[object]", errors):
                value: str | None = (
                    item.get("error_message")
                    if isinstance(item, dict)
                    else None
                )
                if isinstance(value, str) and value:
                    return value

        return None

    @staticmethod
    def _retry_after(
        response: Response,
        body: dict[str, Any] | None,
    ) -> float | None:
        header = response.headers.get("Retry-After", "")
        if header.isdigit():
            return float(header)

        errors = body.get("errors") if body else None
        if isinstance(errors, list):
            for item in cast("list[object]", errors):
                meta = item.get("meta") if isinstance(item, dict) else None
                reset = (
                    meta.get("reset_time") if isinstance(meta, dict) else None
                )

                if isinstance(reset, str):
                    try:
                        moment = datetime.strptime(
                            reset, "%Y/%m/%d %H:%M:%S %z"
                        )
                    except ValueError:
                        continue

                    return max(
                        0.0, (moment - datetime.now(UTC)).total_seconds()
                    )

        return None
