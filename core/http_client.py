import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, cast

import aiohttp

from core.request import Request
from exceptions.soundcloud_errors import *


@dataclass(frozen=True, slots=True)
class RawResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes


class HttpClient:
    TIMEOUT = aiohttp.ClientTimeout(total=10)

    def __init__(self, proxy_endpoint: str | None = None) -> None:
        self._proxy: str | None = proxy_endpoint
        self._session: aiohttp.ClientSession | None = None

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def send(self, request: Request) -> dict[str, Any]:
        raw = await self._execute(request)

        return self._parse_body(raw)

    async def fetch_image(self, request: Request) -> bytes:
        raw = await self._execute(request)

        return raw.body

    def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self.TIMEOUT)

        return self._session

    async def _execute(self, request: Request) -> RawResponse:
        try:
            async with self._get_session().request(
                method=request.method.value,
                url=request.build_url(),
                headers=request.headers,
                data=request.data or None,
                proxy=self._proxy,
            ) as response:
                raw = RawResponse(
                    status=response.status,
                    headers=response.headers,
                    body=await response.read(),
                )
        except (aiohttp.ClientError, TimeoutError) as e:
            raise SoundcloudConnectionError(
                f"Could not reach SoundCloud: {type(e).__name__}"
            ) from e

        if raw.status >= 400:
            raise self._build_error(raw)

        return raw

    @staticmethod
    def _parse_body(raw: RawResponse) -> dict[str, Any]:
        if raw.status == 204 or not raw.body:
            return {}

        try:
            data: Any = json.loads(raw.body)
        except ValueError as e:
            raise InvalidResponseError(
                "SoundCloud returned a non-JSON response"
            ) from e

        if not isinstance(data, dict):
            raise InvalidResponseError(
                f"Expected a JSON object, got {type(data).__name__}"
            )

        return cast("dict[str, Any]", data)

    def _build_error(self, raw: RawResponse) -> ApiError:
        try:
            body = self._parse_body(raw)
        except InvalidResponseError:
            body = {}

        message = str(body.get("error"))

        status = raw.status

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
