from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

from core.server import Server


class HttpServer(Server):
    def __init__(
        self,
        port: int,
        path: str,
    ) -> None:
        super().__init__(
            port=port,
            path=path,
        )

        self.__server = HTTPServer(
            server_address=('', self.port),
            RequestHandlerClass=AuthRequestHandler
        )

        # hack to store the data from response
        self.__server.parent = self

        self.auth_code: str | None = None
        self.state: str | None = None

    def run(
        self,
    ) -> None:
        print(f"Temporary server started at http://localhost:{self.port}. Waiting for callback...")

        self.__server.handle_request()

        print("Callback received! Shutting down the temporary server...")

    def stop(
        self,
    ) -> None:
        self.__server.shutdown()


class AuthRequestHandler(BaseHTTPRequestHandler):
    def do_GET(
        self,
    ) -> None:
        request = urlsplit(self.path)

        if request.path == "/callback":
            params = parse_qs(request.query)

            auth_code = params.get("code", None)
            if isinstance(auth_code, list):
                auth_code = auth_code[0]

            state = params.get("state", None)
            if isinstance(state, list):
                state = state[0]

            # hack to store the data from response
            self.server.parent.auth_code = auth_code
            self.server.parent.state = state

        self.send_response(200)
        self.end_headers()
