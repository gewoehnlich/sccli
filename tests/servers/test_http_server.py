import http.client
import socket
import sys
import time
from collections.abc import Generator
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import FrozenInstanceError, dataclass
from urllib.parse import quote

import pytest

from core.server import Server
from exceptions.servers.callback_timeout_error import CallbackTimeoutError
from exceptions.servers.port_unavailable_error import PortUnavailableError
from exceptions.servers.server_is_already_running_error import (
    ServerIsAlreadyRunningError,
)
from exceptions.servers.server_is_not_started_error import (
    ServerIsNotStartedError,
)
from servers.http_server import HttpServer, _CallbackHandler
from values.callback_result import CallbackResult


@dataclass(frozen=True)
class Response:
    status: int
    headers: dict[str, str]
    body: str


def result(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
) -> CallbackResult:
    return CallbackResult(code=code, state=state, error=error)


def send(
    server: HttpServer,
    target: str,
    method: str = "GET",
) -> Response:
    connection = http.client.HTTPConnection(server.host, server.port, timeout=5)

    try:
        connection.request(method, target)
        response = connection.getresponse()
        body = response.read().decode("utf-8")
        headers = {name.lower(): value for name, value in response.getheaders()}
    finally:
        connection.close()

    return Response(status=response.status, headers=headers, body=body)


@contextmanager
def running(
    host: str = "127.0.0.1",
    port: int = 12345,
    path: str = "/callback",
) -> Generator[HttpServer]:
    instance = HttpServer(host=host, port=port, path=path)
    instance.start()

    try:
        yield instance
    finally:
        instance.stop()


@contextmanager
def waiting(
    server: HttpServer,
    timeout: float = 5.0,
) -> Generator[Future[CallbackResult]]:
    """Run wait_for_callback in a background thread, since it blocks."""
    with ThreadPoolExecutor(max_workers=1) as pool:
        yield pool.submit(server.wait_for_callback, timeout)


def deliver(server: HttpServer, query: str) -> CallbackResult:
    with waiting(server) as future:
        response = send(server, f"{server.path}{query}")
        assert response.status == 200

        return future.result(timeout=5)


@pytest.fixture
def server() -> Generator[HttpServer]:
    with running() as instance:
        yield instance


def test_http_server_is_a_server() -> None:
    assert isinstance(HttpServer(host="127.0.0.1", port=1, path="/"), Server)


def test_constructor_stores_its_arguments_and_binds_nothing() -> None:
    with running() as occupant:
        pending = HttpServer(host="127.0.0.1", port=occupant.port, path="/cb")

    assert (pending.host, pending.path) == ("127.0.0.1", "/cb")


def test_start_reports_the_actual_port() -> None:
    instance = HttpServer(host="127.0.0.1", port=0, path="/callback")
    assert instance.port == 0

    instance.start()
    try:
        assert 0 < instance.port < 65536
    finally:
        instance.stop()


def test_starting_twice_raises() -> None:
    with running() as instance, pytest.raises(ServerIsAlreadyRunningError):
        instance.start()


def test_waiting_before_start_raises() -> None:
    instance = HttpServer(host="127.0.0.1", port=0, path="/callback")

    with pytest.raises(ServerIsNotStartedError):
        instance.wait_for_callback(0.1)


def test_waiting_after_stop_raises() -> None:
    with running() as instance:
        pass

    with pytest.raises(ServerIsNotStartedError):
        instance.wait_for_callback(0.1)


def test_stop_is_safe_before_start_and_when_repeated() -> None:
    instance = HttpServer(host="127.0.0.1", port=0, path="/callback")

    instance.stop()
    instance.start()
    instance.stop()
    instance.stop()


def test_stop_releases_the_port() -> None:
    with running() as first:
        port = first.port

    with running(port=port) as second:
        assert second.port == port


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="SO_REUSEADDR lets two sockets bind the same port on Windows",
)
def test_port_in_use_raises_port_unavailable() -> None:
    with running() as first:
        second = HttpServer(host=first.host, port=first.port, path="/callback")

        with pytest.raises(PortUnavailableError) as exc_info:
            second.start()

        assert isinstance(exc_info.value.__cause__, OSError)

        with pytest.raises(ServerIsNotStartedError):
            second.wait_for_callback(0.1)

    second.start()
    second.stop()


@pytest.mark.parametrize("host", ["127.0.0.1", "localhost"])
def test_serves_on_the_allowed_loopback_hosts(host: str) -> None:
    with running(host=host) as instance:
        assert deliver(instance, "?code=abc&state=xyz") == result("abc", "xyz")


def test_restart_starts_with_a_clean_slate(server: HttpServer) -> None:
    assert deliver(server, "?code=old&state=old") == result("old", "old")

    server.stop()
    server.start()

    with pytest.raises(CallbackTimeoutError):
        server.wait_for_callback(0.2)


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("?code=abc&state=xyz", result("abc", "xyz")),
        ("?state=xyz&code=abc", result("abc", "xyz")),
        ("?code=abc&state=xyz&extra=1&other=2", result("abc", "xyz")),
        # OAuth error response
        (
            "?error=access_denied&state=xyz",
            result(None, "xyz", "access_denied"),
        ),
        (
            "?error=access_denied&error_description=User+denied",
            result(error="access_denied"),
        ),
        # partial parameters
        ("?code=abc", result(code="abc")),
        ("?state=xyz", result(state="xyz")),
        # decoding
        ("?code=a%2Fb%3D%3D&state=x%20y", result("a/b==", "x y")),
        ("?code=a+b&state=x", result("a b", "x")),
        # parameter names are case-sensitive
        ("?CODE=abc&state=xyz", result(None, "xyz")),
        # blank values count as missing
        ("?code=&state=xyz", result(None, "xyz")),
        # repeated parameters are treated as missing, even when the values are equal
        ("?code=a&code=b&state=xyz", result(None, "xyz")),
        ("?code=abc&code=abc&state=xyz", result(None, "xyz")),
        ("?code=abc&state=x&state=y", result("abc", None)),
        # NOTE: a bare request to the callback path ends the wait with an empty result
        ("", result()),
        ("?", result()),
    ],
)
def test_callback_parameters_are_parsed(
    server: HttpServer,
    query: str,
    expected: CallbackResult,
) -> None:
    assert deliver(server, query) == expected


def test_callback_arriving_before_the_wait_is_not_lost(
    server: HttpServer,
) -> None:
    with ThreadPoolExecutor(max_workers=1) as pool:
        pending = pool.submit(send, server, "/callback?code=abc&state=xyz")
        time.sleep(0.2)

        received = server.wait_for_callback(5)

        assert pending.result(timeout=5).status == 200

    assert received == result("abc", "xyz")


def test_waiting_again_returns_the_same_result_immediately(
    server: HttpServer,
) -> None:
    first = deliver(server, "?code=abc&state=xyz")

    assert server.wait_for_callback(0) == first


def test_custom_callback_path() -> None:
    with running(path="/oauth/cb") as custom, waiting(custom) as future:
        assert send(custom, "/callback?code=a&state=b").status == 404
        assert send(custom, "/oauth/cb?code=a&state=b").status == 200

        assert future.result(timeout=5) == result("a", "b")


STRAY_TARGETS = [
    "/",
    "/favicon.ico",
    "/callback/",
    "/Callback",
    "/callback/extra",
    "/callback.html",
    "/oauth/callback",
]


def test_other_paths_get_404_and_do_not_end_the_wait(
    server: HttpServer,
) -> None:
    with waiting(server) as future:
        for target in STRAY_TARGETS:
            response = send(server, f"{target}?code=stolen&state=stolen")

            assert response.status == 404, target

        assert not future.done()

        send(server, "/callback?code=real&state=ok")

        assert future.result(timeout=5) == result("real", "ok")


@pytest.mark.parametrize(
    "method", ["POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
)
def test_only_get_is_supported(server: HttpServer, method: str) -> None:
    with waiting(server) as future:
        response = send(
            server, "/callback?code=stolen&state=stolen", method=method
        )

        assert response.status == 501
        assert not future.done()

        send(server, "/callback?code=real&state=ok")

        assert future.result(timeout=5).code == "real"


def test_idle_connection_does_not_block_the_callback(
    server: HttpServer,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        _CallbackHandler, "timeout", 0.3
    )  # default is 5 s; keep the suite fast

    # a browser pre-connect: connects, sends nothing
    with socket.create_connection((server.host, server.port)):
        started = time.monotonic()
        received = deliver(server, "?code=abc&state=xyz")
        elapsed = time.monotonic() - started

    assert received == result("abc", "xyz")
    assert elapsed < 3


def test_connection_closed_without_a_request_is_ignored(
    server: HttpServer,
) -> None:
    with socket.create_connection((server.host, server.port)):
        pass

    assert deliver(server, "?code=abc&state=xyz") == result("abc", "xyz")


def test_handler_has_a_socket_timeout() -> None:
    # None would let one silent connection freeze the server forever
    assert _CallbackHandler.timeout is not None


# --- timeouts


def test_times_out_when_no_request_arrives(server: HttpServer) -> None:
    started = time.monotonic()

    with pytest.raises(CallbackTimeoutError):
        server.wait_for_callback(0.3)

    elapsed = time.monotonic() - started

    assert 0.25 <= elapsed < 3


def test_zero_timeout_fails_immediately(server: HttpServer) -> None:
    started = time.monotonic()

    with pytest.raises(CallbackTimeoutError):
        server.wait_for_callback(0)

    assert time.monotonic() - started < 1


def test_server_is_still_usable_after_a_timeout(server: HttpServer) -> None:
    with pytest.raises(CallbackTimeoutError):
        server.wait_for_callback(0.2)

    assert deliver(server, "?code=abc&state=xyz") == result("abc", "xyz")


@pytest.mark.parametrize(
    ("target", "status", "text"),
    [
        ("/callback?code=abc&state=xyz", 200, "close this tab"),
        ("/nope", 404, "Not found"),
    ],
)
def test_response_headers_and_body(
    server: HttpServer,
    target: str,
    status: int,
    text: str,
) -> None:
    with waiting(server):
        response = send(server, target)

        if status == 404:
            send(server, "/callback?code=a&state=b")

    assert response.status == status
    assert text in response.body
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert int(response.headers["content-length"]) == len(
        response.body.encode("utf-8")
    )
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["connection"] == "close"


def test_response_does_not_reflect_request_parameters(
    server: HttpServer,
) -> None:
    payload = quote("<script>alert(1)</script>")

    with waiting(server):
        response = send(server, f"/callback?code={payload}&state={payload}")

    assert "script" not in response.body
    assert "alert" not in response.body


def test_callback_result_compares_by_value() -> None:
    assert result("a", "b", None) == result("a", "b", None)
    assert result("a", "b", None) != result("a", "c", None)


def test_callback_result_is_frozen() -> None:
    received = result("a", "b")

    with pytest.raises(FrozenInstanceError):
        received.code = "other"  # pyright: ignore[reportAttributeAccessIssue]
