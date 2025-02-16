import asyncio
from aiohttp import web

class Server:
    def __init__(self) -> None:
        self.future = None

    async def run(self) -> tuple[str, str]:
        self.future = asyncio.get_event_loop().create_future()
        asyncio.create_task(self.start_server())
        print("Server started. Waiting for callback...")
        auth_code, state = await self.future

        await self.shutdown()
        return auth_code, state

    async def start_server(self) -> None:
        app = web.Application()
        app.router.add_get("/callback", self.callback_handler)
        self.runner = web.AppRunner(app)
        await self.runner.setup()

        site = web.TCPSite(self.runner, "localhost", 8080)
        await site.start()

        print("Server is running at http://localhost:8080/callback")
        await self.future

    async def shutdown(self) -> None:
        if self.runner:
            print("Shutting down the temporary server...")
            await self.runner.cleanup()

    async def callback_handler(self, request):
        auth_code = request.query.get("code", None)
        state = request.query.get("state", None)
        if auth_code and state:
            if not self.future.done():
                self.future.set_result((auth_code, state))

        return web.Response(
            text="Callback received. You may close this window."
        )

