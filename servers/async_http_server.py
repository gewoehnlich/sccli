import asyncio
from asyncio import Future
from typing import Any, Self

from aiohttp import web
from aiohttp.web_request import Request

from core.server import Server


class AsyncHttpServer(Server):
    future: Future[Any] | None = None
    runner: Any | None = None

    def __init__(
        self,
        port: int,
        path: str,
    ) -> None:
        super().__init__(
            port=port,
            path=path,
        )

        self.url: str = f"http://localhost:{self.port}{self.path}"

        self.auth_code: str | None = None
        self.state: str | None = None

    def run(
        self,
    ) -> None:
        asyncio.run(self.__run())

    def shutdown(
        self,
    ) -> None:
        asyncio.run(self.__shutdown())

    async def __run(self) -> tuple[str, str]:
        self.future = asyncio.get_event_loop().create_future()
        asyncio.create_task(self.start_server())

        print("Server started. Waiting for callback...")

        result: tuple[str, str] = await self.future
        await self.shutdown()

        return result

    async def start_server(self) -> None:
        app = web.Application()
        app.router.add_get(
            self.path,
            self.callback_handler,
        )

        self.runner = web.AppRunner(app)
        await self.runner.setup()

        site = web.TCPSite(self.runner, "localhost", self.port)

        await site.start()

        print(f"Server is running at {self.url}")

        if self.future is not None:
            await self.future

    async def __shutdown(self) -> None:
        if self.runner:
            print("Shutting down the temporary server...")
            await self.runner.cleanup()

    async def callback_handler(self, request: Request) -> web.Response:
        self.auth_code = request.query.get("code")
        self.state = request.query.get("state")

        if self.auth_code and self.state and self.future is not None and not self.future.done():
            self.future.set_result((self.auth_code, self.state))

        return web.Response(text="Callback received. You may close this window.")
