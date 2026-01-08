import asyncio
from asyncio import Future
from typing import Tuple, Optional, Any, Self
from aiohttp import web
from aiohttp.web_request import Request


class Server:
    future: Optional[Future[Any]] = None
    runner: Optional[Any] = None

    _instance: Self | None = None
    _initialized: bool = False


    def __new__(cls: type[Self], *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def __init__(
        self,
        port: int,
        path: str,
    ) -> None:
        if self._initialized:
            return

        self.port: int = port
        self.path: str = path
        self.url: str = f"http://localhost:{ self.port }{ self.path }"

        self._initialized = True


    async def run(self) -> tuple[str, str]:
        self.future = asyncio.get_event_loop().create_future()
        asyncio.create_task(self.start_server())

        print("Server started. Waiting for callback...")

        result: Tuple[str, str] = await self.future
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

        site = web.TCPSite(
            self.runner,
            "localhost",
            self.port
        )

        await site.start()

        print(f"Server is running at {self.url}")

        if self.future is not None:
            await self.future


    async def shutdown(self) -> None:
        if self.runner:
            print("Shutting down the temporary server...")
            await self.runner.cleanup()


    async def callback_handler(
        self,
        request: Request
    ) -> web.Response:
        auth_code = request.query.get("code")
        state = request.query.get("state")

        if (
            auth_code
            and state
            and self.future is not None
            and not self.future.done()
        ):
            self.future.set_result((auth_code, state))

        return web.Response(
            text="Callback received. You may close this window."
        )
