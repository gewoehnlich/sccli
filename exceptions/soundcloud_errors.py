class SoundcloudError(Exception):
    """Base class for everything the SoundCloud client raises."""


class SoundcloudConnectionError(SoundcloudError):
    """No usable HTTP response: DNS, TLS, refused connection, timeout."""


class InvalidResponseError(SoundcloudError):
    """A success status, but not the JSON object we expect."""


class ApiError(SoundcloudError):
    """SoundCloud answered with an error status."""

    def __init__(
        self,
        status: int,
        message: str,
    ) -> None:
        super().__init__(f"SoundCloud API error {status}: {message}")
        self.status = status
        self.message = message


class OAuthError(ApiError): ...


class InvalidGrantError(OAuthError): ...  # refresh token / code rejected


class UnsupportedGrantError(OAuthError): ...


class InvalidClientError(OAuthError): ...  # wrong client_id / secret


class InvalidScopeError(OAuthError): ...


class UnauthorizedClientError(OAuthError): ...


class BadRequestError(ApiError): ...  # 400


class UnauthorizedError(ApiError): ...  # 401: access token missing/expired


class ForbiddenError(ApiError): ...  # 403


class NotFoundError(ApiError): ...  # 404


class NotAcceptableError(ApiError): ...  # 406


class UnprocessableEntityError(ApiError): ...  # 422: message states the reason


class ServerError(ApiError): ...  # 5xx


class GatewayTimeoutError(ServerError):
    """504: the request may still have been processed. Verify before repeating a write."""


class TooManyRequestsError(ApiError):
    def __init__(
        self,
        status: int,
        message: str,
        spam_warning_urn: str | None,
    ) -> None:
        super().__init__(status, message)
        self.spam_warning_urn = spam_warning_urn
