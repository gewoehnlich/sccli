import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import cast
from urllib.parse import parse_qs, urlsplit

from core.server import Server
from exceptions.servers.callback_timeout_error import CallbackTimeoutError
from exceptions.servers.port_unavailable_error import PortUnavailableError
from exceptions.servers.server_is_already_running_error import ServerIsAlreadyRunningError
from exceptions.servers.server_is_not_started_error import ServerIsNotStartedError
from values.callback_result import CallbackResult


class HttpServer(Server):
    def __init__(self, host: str, port: int, path: str,) -> None:
        super().__init__(host=host, port=port, path=path)

        self._server: _CallbackServer | None = None

    def start(self,) -> None:
        if self._server is not None:
            raise ServerIsAlreadyRunningError()

        try:
            server = _CallbackServer((self.host, self.port), _CallbackHandler)
        except OSError as e:
            raise PortUnavailableError(port=self.port) from e

        server.callback_path = self.path
        self.port = server.server_port
        self._server = server

    def wait_for_callback(self, timeout: float,) -> CallbackResult:
        if self._server is None:
            raise ServerIsNotStartedError()

        deadline = time.monotonic() + timeout

        while self._server.result is None:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise CallbackTimeoutError

            self._server.timeout = remaining
            self._server.handle_request()  # stray requests don't end the loop

        return self._server.result

    def stop(self,) -> None:
        if self._server is not None:
            self._server.server_close()
            self._server = None


class _CallbackServer(HTTPServer):
    result: CallbackResult | None = None
    callback_path: str


class _CallbackHandler(BaseHTTPRequestHandler):
    timeout = 5

    def do_GET(self,) -> None:
        server = cast("_CallbackServer", self.server)
        request = urlsplit(self.path)

        if request.path != server.callback_path:
            self._respond(404, "Not found")
            return

        params = parse_qs(request.query)
        server.result = CallbackResult(
            code=self._single(params, "code"),
            state=self._single(params, "state"),
            error=self._single(params, "error"),
        )
        self._respond(200, "Authentication finished. You can close this tab.")

    @staticmethod
    def _single(params: dict[str, list[str]], key: str,) -> str | None:
        values = params.get(key)
        return values[0] if values is not None and len(values) == 1 else None

    def _respond(self, status: int, message: str,) -> None:
        body = f"<!doctype html><meta charset='utf-8'><p>{message}</p>".encode()

        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)
