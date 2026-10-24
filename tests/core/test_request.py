import json
from unittest.mock import MagicMock

import pytest
import requests
from pytest_mock import MockerFixture

from core.request import Request
from exceptions.soundcloud_errors import *

URL = Request.URL.API


def make_response(
    status: int = 200,
    body: object | None = None,
    raw: bytes | None = None,
) -> requests.Response:
    response = requests.Response()

    response.status_code = status

    if raw is not None:
        response._content = raw
    elif body is not None:
        response._content = json.dumps(body).encode()
    else:
        response._content = b""

    return response


@pytest.fixture
def send_mock(
    mocker: MockerFixture,
) -> MagicMock:
    """Replace the shared session's send() so no real HTTP call is made."""
    return mocker.patch.object(
        Request._session,
        "send",
        return_value=make_response(),
    )


def respond(
    send_mock: MagicMock,
    status: int,
    body: object | None = None,
    raw: bytes | None = None,
) -> None:
    send_mock.return_value = make_response(status, body, raw)


def test_default_headers_are_set() -> None:
    headers = Request(Request.METHOD.GET, URL)._request.headers

    assert headers["Accept"] == "application/json; charset=utf-8"
    assert headers["Content-Type"] == "application/x-www-form-urlencoded"
    assert "Authorization" not in headers


def test_custom_headers_are_not_overridden() -> None:
    headers = Request(
        Request.METHOD.GET,
        URL,
        headers={"Accept": "text/plain", "Content-Type": "application/json"},
    )._request.headers

    assert headers["Accept"] == "text/plain"
    assert headers["Content-Type"] == "application/json"


def test_access_token_sets_authorization_header() -> None:
    headers = Request(
        Request.METHOD.GET,
        URL,
        access_token="abc123",
    )._request.headers

    assert headers["Authorization"] == "OAuth abc123"


def test_params_and_data_are_stored() -> None:
    post_request = Request(
        Request.METHOD.POST,
        URL,
        data={"grant_type": "refresh_token"},
    )._request

    assert post_request.params == {}
    assert post_request.data == {"grant_type": "refresh_token"}

    get_request = Request(
        Request.METHOD.GET,
        URL,
        data={"q": "lofi"},
    )._request

    assert get_request.params == {"q": "lofi"}
    assert get_request.data == {}


def test_params_and_data_default_to_empty() -> None:
    request = Request(Request.METHOD.GET, URL)._request

    assert request.params == {}
    assert request.data == {}


def test_returns_parsed_json_object(
    send_mock: MagicMock,
) -> None:
    respond(send_mock, 200, {"id": 1, "username": "me"})

    assert Request(Request.METHOD.GET, URL).send() == {
        "id": 1,
        "username": "me",
    }


def test_sends_prepared_request_built_from_inputs(
    send_mock: MagicMock,
) -> None:
    respond(send_mock, 200, {})

    Request(
        Request.METHOD.GET,
        URL,
        data={"q": "lofi"},
        access_token="tok",
    ).send()

    prepared = send_mock.call_args.kwargs["request"]

    assert isinstance(prepared, requests.PreparedRequest)
    assert prepared.method == Request.METHOD.GET.value
    assert prepared.url == f"{URL}/?q=lofi"
    assert prepared.headers["Authorization"] == "OAuth tok"


def test_post_data_is_form_encoded(
    send_mock: MagicMock,
) -> None:
    respond(send_mock, 200, {})

    Request(Request.METHOD.POST, URL, data={"a": "1", "b": "2"}).send()

    prepared = send_mock.call_args.kwargs["request"]

    assert prepared.body == "a=1&b=2"


def test_204_returns_empty_dict(
    send_mock: MagicMock,
) -> None:
    respond(send_mock, 204)

    assert Request(Request.METHOD.DELETE, URL).send() == {}


def test_empty_body_returns_empty_dict(
    send_mock: MagicMock,
) -> None:
    respond(send_mock, 200, raw=b"")

    assert Request(Request.METHOD.GET, URL).send() == {}


@pytest.mark.parametrize(
    "exc",
    [
        requests.ConnectionError("boom"),
        requests.Timeout("slow"),
        requests.exceptions.SSLError("tls"),
    ],
)
def test_request_exceptions_become_connection_error(
    send_mock: MagicMock,
    exc: requests.RequestException,
) -> None:
    send_mock.side_effect = exc

    with pytest.raises(SoundcloudConnectionError) as info:
        Request(Request.METHOD.GET, URL).send()

    assert info.value.__cause__ is exc
    assert type(exc).__name__ in str(info.value)


def test_non_json_success_body_raises_invalid_response(
    send_mock: MagicMock,
) -> None:
    respond(send_mock, 200, raw=b"<html>nope</html>")

    with pytest.raises(InvalidResponseError):
        Request(Request.METHOD.GET, URL).send()


@pytest.mark.parametrize(
    "body",
    [
        [1, 2, 3],
        "text",
        42,
        None,
    ],
)
def test_non_object_json_raises_invalid_response(
    send_mock: MagicMock,
    body: object,
) -> None:
    send_mock.return_value = make_response(200, raw=json.dumps(body).encode())

    with pytest.raises(InvalidResponseError):
        Request(Request.METHOD.GET, URL).send()


@pytest.mark.parametrize(
    "status",
    [
        400,
        401,
    ],
)
@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("invalid_grant", InvalidGrantError),
        ("unsupported_grant", UnsupportedGrantError),
        ("unsupported_grant_type", UnsupportedGrantError),
        ("invalid_client", InvalidClientError),
        ("invalid_scope", InvalidScopeError),
        ("unauthorized_client", UnauthorizedClientError),
    ],
)
def test_oauth_errors(
    send_mock: MagicMock,
    status: int,
    message: str,
    expected: type[ApiError],
) -> None:
    respond(send_mock, status, {"message": message})

    with pytest.raises(ApiError) as info:
        Request(Request.METHOD.POST, URL).send()

    assert type(info.value) is expected


@pytest.mark.parametrize(
    "status",
    [
        403,
        404,
        422,
        500,
    ],
)
def test_oauth_message_ignored_for_other_statuses(
    send_mock: MagicMock,
    status: int,
) -> None:
    respond(send_mock, status, {"message": "invalid_grant"})

    with pytest.raises(ApiError) as info:
        Request(Request.METHOD.POST, URL).send()

    assert type(info.value) is not InvalidGrantError


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (400, BadRequestError),
        (401, UnauthorizedError),
        (403, ForbiddenError),
        (404, NotFoundError),
        (406, NotAcceptableError),
        (422, UnprocessableEntityError),
        (504, GatewayTimeoutError),
    ],
)
def test_status_code_mapping(
    send_mock: MagicMock,
    status: int,
    expected: type[ApiError],
) -> None:
    respond(send_mock, status, {"message": "something went wrong"})

    with pytest.raises(ApiError) as info:
        Request(Request.METHOD.GET, URL).send()

    assert type(info.value) is expected


@pytest.mark.parametrize(
    "status",
    [
        500,
        502,
        503,
    ],
)
def test_other_5xx_become_server_error(
    send_mock: MagicMock,
    status: int,
) -> None:
    respond(send_mock, status, {"message": "down"})

    with pytest.raises(ApiError) as info:
        Request(Request.METHOD.GET, URL).send()

    assert type(info.value) is ServerError


@pytest.mark.parametrize(
    "status",
    [
        402,
        405,
        409,
        418,
    ],
)
def test_unmapped_4xx_become_generic_api_error(
    send_mock: MagicMock,
    status: int,
) -> None:
    respond(send_mock, status, {"message": "meh"})

    with pytest.raises(ApiError) as info:
        Request(Request.METHOD.GET, URL).send()

    assert type(info.value) is ApiError


def test_429_with_spam_warning_urn(
    send_mock: MagicMock,
) -> None:
    respond(
        send_mock,
        429,
        {"message": "slow down", "spam_warning_urn": "soundcloud:spam:1"},
    )

    with pytest.raises(TooManyRequestsError):
        Request(Request.METHOD.GET, URL).send()


def test_429_without_spam_warning_urn(
    send_mock: MagicMock,
) -> None:
    respond(send_mock, 429, {"message": "slow down"})

    with pytest.raises(TooManyRequestsError):
        Request(Request.METHOD.GET, URL).send()


def test_error_with_empty_body_still_maps_by_status(
    send_mock: MagicMock,
) -> None:
    respond(send_mock, 404, raw=b"")

    with pytest.raises(NotFoundError):
        Request(Request.METHOD.GET, URL).send()


def test_error_without_message_key_still_maps_by_status(
    send_mock: MagicMock,
) -> None:
    respond(send_mock, 403, {"errors": []})

    with pytest.raises(ForbiddenError):
        Request(Request.METHOD.GET, URL).send()
