import asyncio
from aiohttp import web
from aiohttp.web_request import Request
from asyncio import Future
from typing import Tuple, Optional, Any

class Server:
    def __init__(self) -> None:
        self.future: Optional[Future[Any]] = None

    async def run(self) -> tuple[str, str]:
        self.future = asyncio.get_event_loop().create_future()
        asyncio.create_task(self.start_server())

        print("Server started. Waiting for callback...")

        result: Tuple[str, str] = await self.future
        await self.shutdown()

        return result

    async def start_server(self) -> None:
        app = web.Application()
        app.router.add_get("/callback", self.callback_handler)
        self.runner = web.AppRunner(app)
        await self.runner.setup()

        site = web.TCPSite(self.runner, "localhost", 8080)
        await site.start()

        print("Server is running at http://localhost:8080/callback")
        
        if self.future is not None:
            await self.future

    async def shutdown(self) -> None:
        if self.runner:
            print("Shutting down the temporary server...")
            await self.runner.cleanup()

    async def callback_handler(self, request: Request) -> web.Response:
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

